
// The reference of players must be kept
players = {};
const GamePhase = Object.freeze({"INIT":"INIT", "CHOSE":"CHOSE", "DRAW":"DRAW", "SCORE":"SCORE", "END": "END"});
var gamePhase = "UNKNOWN"
var socket = io();


function refreshPlayers(playersData) {
    $("#playerList").empty()
    for (var p in players) delete players[p]; // only deleting content to keep reference.
    for (const player of playersData) {
        p = new Player(player["name"], player["score"], player["color"], player["status"], player["ready"], player["isPlaying"]);
        addPlayer(p);
    }
}

function addPlayer(player) {
    players[player.name] = player;
}

function setPlayersNotDrawing() {
    for (let playerName in players) {
        players[playerName].isDrawing = false;
    }
}

function setTime(timeVal) {
    $("#time").text(timeVal);
}

function removeTime() {
    $("#time").text("");
}

function initPictionnary(roomName, playerName) {
    discussion = new Discussion();

    width = 1300;
    height = 600;

    // Create graphic stage
    stage = new Stage(width, height, 3, players, playerName);
    stage.readyButton.on("pointerdown", function() {players[playerName].toggleReady(true);});

    const drawingArea = new PIXI.Graphics();
    drawingArea.interactive = true;
    drawingArea.buttonMode = false;

    drawing = new DrawingArea(drawingArea, width, height);

    drawingArea.on("mousedown", function(ev){
        if (playerName in players && players[playerName].isDrawing) {
            var x = ev.data.global.x;
            var y = ev.data.global.y;
            socket.emit('draws', x, y);
            drawing.draw(x, y, true);
        }
    });

    drawingArea.on("mouseup", function(ev){
        if (playerName in players && players[playerName].isDrawing) {
            drawing.onMouseUp();
            socket.emit("mouseup");
        }
    });

    drawingArea.on('mousemove', function(ev) {
        if (playerName in players && players[playerName].isDrawing) {
            var x = ev.data.global.x;
            var y = ev.data.global.y;
            var buttons = ev.data.buttons;
            if (buttons == 1) {
                socket.emit('draws', x, y);
                drawing.draw(x, y);
            }
        }
    });

    stage.app.stage.addChild(drawingArea);

    $( document ).ready(function() {
        $("#discussionForm").submit(function( event ) {
            var message = $("#msgInput").val();
            //discussion.playerSendsMessage(playerName, message);
            $("#msgInput").val('');
            console.log("send " + message)
            socket.emit('sendMessage', message);
            event.preventDefault();
        });
    });

    socket.on('connect', function() {
        socket.emit('join', roomName, playerName);

        socket.on('initInfo', initInfo => {
            console.log("Init info", initInfo);
            // remove widgets
            stage.clearWidgets();
            refreshPlayers(initInfo["players"]);
            drawing.drawSteps(initInfo["drawing"]);
            var phase = initInfo["phase"];
            gamePhase = phase;

            for (const msg of initInfo["messages"]) {
                discussion.playerSendsMessage(msg["playerName"], msg["content"]);
            }

            if (phase == GamePhase.INIT) {
                // Ajouter bouton prêt sur la zone de draw
                stage.showReadyButton(true);
            }
            else if (phase == GamePhase.DRAW && "word" in initInfo) {
                players[playerName].word = initInfo["word"];
            }
        });

        socket.on(GamePhase.CHOSE, data => {
            console.log("Start choice phase " + data);
            if (gamePhase == GamePhase.INIT) {
                stage.showReadyButton(false);
            }
            gamePhase = GamePhase.CHOSE;
            setPlayersNotDrawing();
            drawing.clear();
            players[data["currPlayer"]].setPlaying(true);
        });

       socket.on(GamePhase.DRAW, currentPlayerName => {
            stage.removeOverlayMessage();
            if (players[playerName].isPlaying) {
                stage.showOverlayMessage("You are drawing : " + players[playerName].word);
                players[playerName].isDrawing = true;
            }
            else {
                stage.showOverlayMessage(currentPlayerName + " is drawing");
            }
       });

       socket.on(GamePhase.SCORE, scoreInfos => {
            console.log(scoreInfos);
            stage.removeOverlayMessage();
            removeTime();
            scoreStr = "Scores :\n"
            for (let playerName in scoreInfos) {
                players[playerName].setPlaying(false);
                players[playerName].isDrawing = true;
                scoreStr += playerName + ": " + players[playerName].score + "+" + scoreInfos[playerName].scoreAdded + " (" + scoreInfos[playerName].scoreCalc + ")\n";
                players[playerName].addScore(scoreInfos[playerName].scoreAdded);
            }
            stage.showOverlayMessage(scoreStr);
       });

        socket.on("wordList", words => {
            console.log("Words : ", words);
            stage.showOverlayMessage("Chose a word to draw :");
            stage.showWordButtons(words);
        });

        socket.on(GamePhase.END, data => {
            console.log("End game");
            stage.removeOverlayMessage();
            scoreStr = "Fin de la partie\nScores :\n"

            let scores = {};
            for (let playerName in players) {
                players[playerName].setPlaying(false);
                players[playerName].isDrawing = true;
                scores[playerName] = players[playerName].score;
            }
            scoresSorted = Object.keys(scores).sort(function(a,b){return scores[a]-scores[b]})
            console.log("Scoresss " + scoresSorted);
            let i = 1;
            for (const playerName of scoresSorted) {
                scoreStr += "#" + i + " " + playerName + " " + players[playerName].score + "\n";
                i++;
            }

            stage.showOverlayMessage(scoreStr);

        })

        socket.on('playerEnters', playerData => {
            console.log("PLAYER ENTERS", playerData);
            p = new Player(playerData["name"], playerData["score"], playerData["color"], playerData["status"],
                playerData["reader"], playerData["isPlaying"]);
            addPlayer(p);
        });

        socket.on('playerDisconnects', playerName => {
            console.log("Player leaves", playerName);
            players[playerName].updateStatus("disconnected");
            if (gamePhase == GamePhase.INIT) {
                players[playerName].setReady(false, false);
            }
        });

         socket.on('playerReconnects', playerName => {
            console.log("Player reconnects", playerName);
            players[playerName].updateStatus("active");
        });

        socket.on("draws", mousePos => {
            //console.log("Receive drawing", mousePos);
            drawing.draw(mousePos["x"], mousePos["y"]);
        });

        socket.on("mouseup", mousePos => {
            drawing.prevX = null;
            drawing.prevY = null;
        });

        socket.on("receiveMessage", msgInfo => {
            console.log(msgInfo);
            if ("server" in msgInfo) {
                discussion.addServerMessage(msgInfo["content"]);
            } else {
                discussion.playerSendsMessage(msgInfo["playerName"], msgInfo["content"]);
            }
            discussion.scrollToBottom();
        });

        socket.on("timeLeft", timeLeft => {
            setTime(timeLeft);
        });

        socket.on("playerReady", readyInfo => {
            players[readyInfo["playerName"]].setReady(readyInfo["isReady"], false);
        });

        socket.on("overlayMessage", message => {
            stage.showOverlayMessage(message);
        });

        socket.on("removeOverlayMessage", data => {
            stage.removeOverlayMessage();
        });
    });

}

function removePlayer() {
}