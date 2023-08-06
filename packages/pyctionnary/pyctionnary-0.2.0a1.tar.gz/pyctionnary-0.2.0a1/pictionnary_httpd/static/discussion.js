class Discussion {
    constructor() {}

    addMessage(message, cssStyles={"font-style": "normal", "color": "black"}) {
        var style = "";
        for  (let styleProp in cssStyles) {
            style += styleProp + ": " + cssStyles[styleProp] + ";"
        }
        $("#messages").append("<div style='" + style + "'>" + message + "</div>")
    }

    notifyPlayerJoin(playerName) {}
    notifyPlayerLeaves(playerName) {}
    notifyPlayerReconnect(playerName) {}
    playerSendsMessage(playerName, message) {
        this.addMessage("<b>" + playerName + "</b>" + ": " + message);
        this.scrollToBottom();
    }

    addServerMessage(message) {
        this.addMessage(message, {"font-style": "normal", "color": "#358835"});
    }

    scrollToBottom() {
        $("#messages").scrollTop($("#messages").prop("scrollHeight"));
    }
}


