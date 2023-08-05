class Player {
  constructor(name, score, color, status, ready, isPlaying) {
    this.name = name;
    this.score = score;
    this.color = color;
    this.status = status;
    this.ready = ready;
    this.colorDisconnected = "grey";
    this.colorOk = "white";
    this.colorPlaying = "green";
    this.isPlaying = isPlaying;
    this.isDrawing = true;
    this.word = null;

    $("#playerList").append(`<div class="playerBox"
    id="${this.name}">${this.name} <span id="${this.name}_score">${this.score}</span>
    <span id="${this.name}_status"></span></div>`);

    if (this.ready) {
        if (this.isPlaying) {
            this.setBackground(this.colorPlaying);
        } else {
            this.setBackground(this.colorOk);
        }
     } else {
        this.setBackground(this.colorDisconnected);
     }
  }

  addScore(scoreAdd) {
    this.score += scoreAdd;
    $("#" + this.name + "_score").text(this.score);
  }

  updateStatus(status) {
    this.status = status;
    if (status == "disconnected") {
        $("#" + this.name + "_status").text(" - Disconnected");
        this.setBackground(this.colorDisconnected);
    }
    else if (status == "active") {
        $("#" + this.name + "_status").text("");
        if (this.ready) {
            if(this.isPlaying) {
                this.setBackground(this.colorPlaying);
            }
            else {
                this.setBackground(this.colorOk);
            }
        }
    }
  }

  toggleReady(notify=false) {
    this.setReady(!this.ready, notify);
  }

  setPlaying(isPlaying) {
    this.isPlaying = isPlaying;
    if (isPlaying) {
        this.setBackground(this.colorPlaying);
    } else {
        this.setBackground(this.colorOk);
    }
  }

  setBackground(color) {
    $("#" + this.name).css("background-color", color);
  }

  setReady(isReady, notify=false) {
    this.ready = isReady;
    if (notify) {
        socket.emit('playerReady', isReady);
    }
    if (isReady) {
        this.setBackground(this.colorOk);
    }
    else {
        this.setBackground(this.colorDisconnected);
    }
  }
}