class Stage {
    constructor(width, height, wordsButtonCount, players, playerName) {
        this.playerName = playerName;
        this.players = players;
        this.app = new PIXI.Application({width: width, height: height});
        this.app.renderer.plugins.interaction.moveWhenInside = true;
        //Add the canvas that Pixi automatically created for you to the HTML document
        $("#gameContainer").append(this.app.view);

        this.width = width;
        this.height = height;

        this.overlayMessage = new PIXI.Text("Empty",{fontFamily : 'Arial',
            fontSize: 24, fill : 0x000000, align : 'center'});
        this.overlayMessage.y = 100;

        let textureIdle = PIXI.Texture.fromImage(Flask.url_for('static', {filename:"pret_down.jpg"}));
        let textureDown = PIXI.Texture.fromImage(Flask.url_for('static', {filename:"pret_up.jpg"}));
        this.readyButton = new Button(textureIdle, textureDown, this.width / 2 - textureIdle.width,
            this.height / 2 - textureIdle.height);

        let stage = this;
        this.wordButtons = []
        for (let i = 0 ; i < wordsButtonCount ; i++) {
            //this.words.push(new PIXI.Text("empty",{fontFamily : 'Arial',
            //fontSize: 24, fill : 0x000000, align : 'center'}));
            //this.wordButtons.push(new Button(PIXI.Texture.WHITE, PIXI.Texture.WHITE, 0, 0, 0xAAAAAA, 0x777777));
            this.wordButtons.push(new TextButton("empty", 0, 0, 0xAAAAAA, 0x777777));
            this.wordButtons[i].on("pointerdown", function() {stage.wordChosed(this.text.text)});
        }
    }

    showReadyButton(show) {
        if (show) {
            this.app.stage.addChild(this.readyButton);
        }
        else {
            this.readyButton.setUp();
            this.app.stage.removeChild(this.readyButton);
        }
    }

    showOverlayMessage(message) {
        this.overlayMessage.text = message;
        this.overlayMessage.x = this.width / 2 - this.overlayMessage.width /2;
        this.app.stage.addChild(this.overlayMessage);
    }

    removeOverlayMessage() {
        this.app.stage.removeChild(this.overlayMessage);
    }

    wordChosed(word) {
        console.log(this.players);
        this.players[this.playerName].word = word;
        socket.emit('wordChosed', word);
        this.removeWordButtons();
        //this.removeOverlayMessage();
    }

    showWordButtons(words) {
        let cumHeight = 0;
        for (let i = 0 ; i < words.length ; i++) {
            this.wordButtons[i].updateText(words[i]);

            this.wordButtons[i].setPosition(this.width / 2,
                this.overlayMessage.y + 40 + this.wordButtons[i].height / 2 + cumHeight)

            cumHeight += this.wordButtons[i].height + 10;

            this.app.stage.addChild(this.wordButtons[i]);
            this.app.stage.addChild(this.wordButtons[i].text);
        }
    }

    removeWordButtons() {
        for (let i = 0 ; i < this.wordButtons.length ; i++) {
            this.app.stage.removeChild(this.wordButtons[i])
            this.app.stage.removeChild(this.wordButtons[i].text)
        }
    }

    clearWidgets() {
        this.removeOverlayMessage();
        this.removeWordButtons();
    }

}


class DrawingArea {
    constructor(drawingArea, frameWidth, frameHeight) {
        this.drawingArea = drawingArea;
        this.frameWidth = frameWidth;
        this.frameHeight = frameHeight;
        this.prevX = null;
        this.prevY = null;

        this.clear();
    }

    draw(mouseX, mouseY, drawPoint=false) {
        this.drawingArea.beginFill(0x000000);
        if (this.prevX == null || this.prevY == null || drawPoint) {
            //console.log("Draw RECT move")
            this.drawingArea.lineStyle(0);
            this.drawingArea.drawCircle(mouseX, mouseY, 2.5);
        }
        else {
            //console.log("Draw LINE")
            this.drawingArea.lineStyle(5);
            this.drawingArea.moveTo(this.prevX, this.prevY);
            this.drawingArea.lineTo(mouseX, mouseY);
        }
        this.drawingArea.endFill();
        this.prevX = mouseX;
        this.prevY = mouseY;
    }

    onMouseUp() {
        drawing.prevY = null;
        drawing.prevX = null;
    }

    drawSteps(drawingSteps) {
        console.log("Drawing whole drawing");
        for (let step in drawingSteps) {
            if (drawingSteps[step]["event"] == "draws") {
                this.draw(drawingSteps[step]["x"], drawingSteps[step]["y"]);
            }
            else if (drawingSteps[step]["event"] == "mouseup") {
                this.onMouseUp();
            }
        }
    }

    clear() {
        this.drawingArea.beginFill(0xFFFFFF);
        this.drawingArea.drawRect(3, 3, this.frameWidth - 6, this.frameHeight - 6);
        this.drawingArea.endFill();
    }

}