class Button extends PIXI.Sprite {
    constructor(textureIdle, textureDown, posX, posY, tintUp=0xFFFFFF, tintDown=0xFFFFFF, autoUp=false) {
        super(textureIdle);
        this.buttonMode = true;
        this.interactive = true;
        this.anchor.set(0.5);
        this.x = posX;
        this.y = posY;
        this.isDown = false;
        this.autoUp = autoUp;
        this.tintUp = tintUp;
        this.tintDown = tintDown;
        this.tint = this.tintUp;

        this.textureIdle = textureIdle;
        this.textureDown = textureDown;
        this.on('pointerdown', this.onButtonDown);
        if (autoUp) {
            this.on('pointerup', this.onButtonUp);
        }
    }

    setUp() {
        this.isDown = false;
        this.texture = this.textureIdle;
        this.tint = this.tintUp;
    }

    onButtonDown() {
        if (this.isDown) {
            this.isDown = false;
            this.texture = this.textureIdle;
            this.tint = this.tintUp;
        }
        else {
            console.log("Down", this.textureDown);
            this.isDown = true;
            this.texture = this.textureDown;
            this.alpha = 1;
            this.tint = this.tintDown;
        }
    }

    onButtonUp() {
        this.isDown = false;
        //if (this.isOver) {
         //   this.texture = textureButtonOver;
        //}
        //else {
        this.texture = this.textureIdle;
        //}
    }
}

class TextButton extends Button {
    constructor(text, posX, posY, backgroundColorUp, backgroundColorDown, autoUp=false) {
        super(PIXI.Texture.WHITE, PIXI.Texture.WHITE, posX, posY, backgroundColorUp, backgroundColorDown, autoUp);
        this.text = new PIXI.Text(text,{fontFamily : 'Arial',
            fontSize: 24, fill : 0x000000, align : 'center'});

        this.buttonMargin = 20;

        this.updateWidth();
        this.setPosition(posX, posY);
    }

    setPosition(x, y) {
        this.x = x;
        this.y = y;
        this.text.x = x - this.text.width / 2;
        this.text.y = y - this.text.height / 2;
    }

    updateWidth() {
        this.width = this.text.width + this.buttonMargin;
        this.height = this.text.height + this.buttonMargin;
    }

    updateText(text) {
        this.text.text = text;
        this.text.updateText();
        this.updateWidth();
    }
}