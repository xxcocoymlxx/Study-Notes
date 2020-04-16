function randint(n){ return Math.round(Math.random()*n); }
function rand(n){ return Math.random()*n; }

//the whole map of the world
class World {
    constructor(canvas){
        this.canvas = canvas;
        this.mouseClick = false;
	
        this.actors=[]; // all actors on this stage (monsters, player, boxes, ...)
        this.player=null; // a special actor, the player
        this.enemyRemain = 50;
        this.gameOver = false;
	
		// the logical width and height of the world, logical space 10000x10000.
		this.width=5000;
        this.height=5000;

        //initiate stage's position and size
        this.stage = new Stage(this, canvas);

        // Add the player to the center of the stage
        this.addPlayer(new Player(this, Math.floor(this.width/2), Math.floor(this.height/2)));

		//Add in some Boxes
		var total=300;
		while(total>100){
			var x=Math.floor((Math.random()*this.width)); 
			var y=Math.floor((Math.random()*this.height)); 
			if(this.getActor(x,y)===null){
                var width = randint(150)+50;
                var height = randint(150)+50;
				var colour= "blue";
				var position = new Pair(x,y);
				var box = new Box(this, position, colour, width, height);
				this.addActor(box);
				total--;
            }
        }

        //Add in some ammo boxes
		while(total>0){
			var x=Math.floor((Math.random()*this.width)); 
			var y=Math.floor((Math.random()*this.height)); 
			if(this.getActor(x,y)===null){
                // var width = randint(30);
                // var height = randint(30);
				var colour= "brown";
				var position = new Pair(x,y);
				var box = new AmmoBox(this, position, colour, 50, 50);
				this.addActor(box);
				total--;
            }
        }

        //add in four bundaries
        var upPosition = new Pair(0, 0);
        var leftPosition = new Pair(0, 0);
        var rightPosition = new Pair(this.width - 10, 0);
        var downPosition = new Pair(0, this.height - 10);
        var upBox = new Boundary(this, upPosition, "black", this.width, 10);
        var leftBox = new Boundary(this, leftPosition, "black", 10, this.height);
        var rightBox = new Boundary(this, rightPosition, "black", 10, this.height);
        var downBox = new Boundary(this, downPosition, "black", this.width, 10);

        this.addActor(upBox);
        this.addActor(leftBox);
        this.addActor(rightBox);
        this.addActor(downBox);


        //add in some enemyAI
        total = this.enemyRemain;
        while(total>0){
			var x=Math.floor((Math.random()*this.width)); 
			var y=Math.floor((Math.random()*this.height)); 
			if(this.getActor(x,y)===null){
				var colour= "green";
                var position = new Pair(x,y);
                var velocity = new Pair(0, 0);
                //var target = new Pair(this.player.position.x, this.player.position.y);
                //enemy.headTo(target);
				var enemy = new EnemyAI(this, position, velocity, colour, 30);
				this.addActor(enemy);
				total--;
            }
        }

	}

    addPlayer(player){
		this.addActor(player);
		this.player=player;
    }
    
    removePlayer(){
		this.removeActor(this.player);
		this.player=null;
    }
    
    addActor(actor){
		this.actors.push(actor);
	}

	removeActor(actor){
		var index=this.actors.indexOf(actor);
		if(index!=-1){
			this.actors.splice(index,1);
		}
	}

    // Take one step in the animation of the game.  Do this by asking each of the actors to take a single step. 
	// NOTE: Careful if an actor died, this may break!
	step(){
		for(var i=0;i<this.actors.length;i++){
			this.actors[i].step();
        }
    }
    

    draw(){
		var context = this.canvas.getContext('2d');
		context.clearRect(0, 0, this.width, this.height);
		for(var i=0;i<this.actors.length;i++){
			this.actors[i].draw(context);
        }
        
        context.fillStyle = "black";
        context.font = 'bold 20px Arial';
        context.fillText("Ammo:"+this.player.gun.ammo,10,20);
        context.fillText("Coordinates:"+(this.player.position.x-2500)+","+(this.player.position.y-2500),10,40);
        context.fillText("Life:"+this.player.life+"/10",10,60);
        context.fillText("Enemy Left:"+this.enemyRemain+"/50",10,80);
        if(this.player.life <= 0){
            context.font = 'bold 95px Arial';
            context.fillStyle = "black";
            context.fillText("GAME OVER",430,350);
        }
        if(this.enemyRemain <= 0){
            context.font = 'bold 95px Arial';
            context.fillStyle = "black";
            context.fillText("YOU WIN!!!",430,350);
        }


        return;
        
	}



	// return the first actor at coordinates (x,y) return null if there is no such actor
	getActor(x, y){
		for(var i=0;i<this.actors.length;i++){
			if(this.actors[i].x==x && this.actors[i].y==y){
				return this.actors[i];
			}
		}
		return null;
	}


	//check the given point is in the stage.
	positionOnStage(x, y){
        if(x - this.stage.position.x < this.stage.width && x > this.stage.position.x){
			if (y - this.stage.position.y < this.stage.height && y > this.stage.position.y){
				return true;
			} 
        }else{
            return false;
        }
    }

}























//view of the whole world
class Stage {
    constructor(world, canvas){
		this.world = world;

        this.width=canvas.width;
        this.height=canvas.height;

        var stageX = Math.floor(this.world.width/2) - Math.floor(this.width/2);
        var stageY = Math.floor(this.world.height/2) - Math.floor(this.height/2);
        if(stageX <= 0){
            stageX = 0;
        }
        if(stageY <= 0){
            stageY = 0;
        }
        this.position = new Pair(stageX, stageY);
    }
}









class Pair {
	constructor(x,y){
		this.x=x; this.y=y;
	}

	toString(){
		return "("+this.x+","+this.y+")";
	}

	normalize(){
		var magnitude=Math.sqrt(this.x*this.x+this.y*this.y);
		this.x=this.x/magnitude ;
		this.y=this.y/magnitude;
	}
}























//user's charactor
class Player {
    constructor(world, x, y){
		this.position = new Pair(x, y);
		this.radius = 20;
        this.world = world;
        this.colour = "red";
        this.life = 30;
        this.enemyKilled = 0;


        this.intPosition();

        this.gun = new Gun(this.world, this.position, this.colour, 20, 30, 10);

    }

    toString(){
		return this.position.toString();
    }

    intPosition(){
		this.x = Math.round(this.position.x);
		this.y = Math.round(this.position.y);
    }


    parseGunPosition(mouseX, mouseY){
        var xDiff = mouseX - 759;
        var yDiff = mouseY - 452;
        var distance = Math.sqrt(xDiff*xDiff+yDiff*yDiff);
        var rate = Math.round(distance/this.gun.length);
        
        var gunPositionX = 700 + Math.round(xDiff/rate);
        var gunPosttionY = 300 + Math.round(yDiff/rate);

        this.gun.position = new Pair(gunPositionX, gunPosttionY);

    }

    fire(mouseX, mouseY){
        //initiate a new bullet actor in the world

        //check if there are enough bullets
        if(this.gun.ammo > 0){
           //parse the mouse position into the real world
            var mouseInWorldX = mouseX - 59 + this.world.stage.position.x; 
            var mouseInWorldY = mouseY - 152 + this.world.stage.position.y;
            var bulletPositionX = this.gun.position.x + this.world.stage.position.x
            var bulletPositionY = this.gun.position.y + this.world.stage.position.y

            var target = new Pair(mouseInWorldX, mouseInWorldY);
            var bPosition = new Pair(bulletPositionX, bulletPositionY);
            var velocity = new Pair(0, 0);
            var bullet = new Bullet(this.world, bPosition, velocity, this.colour, 5);
            bullet.headTo(target);
            this.world.addActor(bullet); 
            this.gun.ammo -= 1;
        }

        

    }

    //check if the given enemy hits the player
    positionHit(x, y){  
        return false;
    }

    enemyHit(x, y){
        var xDiff = Math.abs(this.position.x - x);
        var yDiff = Math.abs(this.position.y - y);
        var centerDiff = Math.sqrt(xDiff*xDiff+yDiff*yDiff);

        if (centerDiff > this.radius + 20){
            return false;
        }else{
            return true;
        }
    }



    hitOnBox(x, y){
        for(var i=0;i<this.world.actors.length;i++){
			if(this.world.actors[i].positionHit(x, y)){
                if(this.world.actors[i] instanceof AmmoBox){
                    this.world.actors[i].removeActor();
                }
                return true;
            }
        }
        return false;
    }

    removeActor(){
        this.world.removeActor(this);
    }


    isHit(){
        this.life -= 1;
        if(this.life <= 0){
            this.world.actors = [];
            this.world.gameOver = true;
        }
        return;
    }


    step(){
        //update player's position by updates the stage's position
        //first check if the player hits a box
        if (this.world.keys && this.world.keys[68]) {
            if(!this.hitOnBox(this.position.x + this.radius, this.position.y)){
                this.world.stage.position.x += 5; 
                this.position.x += 5;
            }
            
        }
        if (this.world.keys && this.world.keys[65]) {
            if(!this.hitOnBox(this.position.x - this.radius, this.position.y)){
                this.world.stage.position.x -= 5; 
                this.position.x -= 5;
            }
            
        }
        if (this.world.keys && this.world.keys[83]) {
            if(!this.hitOnBox(this.position.x, this.position.y + this.radius)){
                this.world.stage.position.y += 5; 
                this.position.y += 5; 
            }
            
        }
        if (this.world.keys && this.world.keys[87]) {
            if(!this.hitOnBox(this.position.x, this.position.y - this.radius)){
                this.world.stage.position.y -= 5; 
                this.position.y -= 5;
            }
            
        }


        //step for mouse event
        if(this.world.mouseClick){
            this.world.mouseClick = false;
            this.fire(this.world.mouseClickX, this.world.mouseClickY);
            this.world.timer = setTimeout(function(){this.world.mouseClick = true;}, 100);
        }

        return;
    }

    draw(context){
		var newPositionX = Math.floor(this.world.stage.width/2);
        var newPositionY = Math.floor(this.world.stage.height/2);

        context.fillStyle = "red";
         
        context.beginPath(); 
        context.arc(newPositionX, newPositionY, this.radius, 0, 2 * Math.PI, false); 

        
        context.arc(this.gun.position.x, this.gun.position.y, 10, 0, 2 * Math.PI, false); 
        context.fill(); 

        return;
    }


}























class Gun{
    constructor(world, position, colour, length, ammo, radius){
        this.world = world;
        this.position = position;
        this.colour = colour;
        this.radius = radius;
        this.ammo = ammo;
        this.length = length;
    }

}


















class Bullet {
    constructor(world, position, velocity, colour, radius){
        this.world = world;
		this.position = position;

		this.velocity = velocity;
		this.colour = colour;
        this.radius = radius;
        this.range = 500;
    }


    headTo(position){
		this.velocity.x=(position.x-this.position.x);
		this.velocity.y=(position.y-this.position.y);
		this.velocity.normalize();
    }
    

    toString(){
		return this.position.toString() + " " + this.velocity.toString();
    }


    //check if the given position hits the bullet
    positionHit(x, y){
        //bullet can not hit bullet
        return false;
    }
    
    removeActor(){
        this.world.removeActor(this);
    }

    isHit(){
        //bullet can not be hit
        return;
    }

    step(){
		this.position.x=this.position.x+17*this.velocity.x;
        this.position.y=this.position.y+17*this.velocity.y;

        this.range = this.range - Math.sqrt(17*this.velocity.x*17*this.velocity.x + 17*this.velocity.y*17*this.velocity.y)
        if(this.range <= 0){
            //the bullet run out of range;
            this.removeActor();
            return;
        }
        for(var i=0;i<this.world.actors.length;i++){
            if(this.world.actors[i].positionHit(this.position.x, this.position.y)){
                this.world.actors[i].isHit();
                this.world.removeActor(this);   
            }    
            
        }
        
			
    }


    draw(context){
        //first check if the Box is in the stage;
		if(this.world.positionOnStage(this.position.x, this.position.y)){
			//the box is on the stage, initiate a new box to represent its status on stage;
            var newPositionX = this.position.x - this.world.stage.position.x;
            var newPositionY = this.position.y - this.world.stage.position.y;
            context.fillStyle = this.colour;
		    context.beginPath(); 
		    context.arc(newPositionX, newPositionY, this.radius, 0, 2 * Math.PI, false); 
		    context.fill();
            return;
		}else{// if it is not on the stage, do not draw it.
			return;
		}

		   
	}
}



















//Box class can't move so it doesn't have step
class Box {
    constructor(world, position, colour, width, height){
        this.world = world;
        this.position = position;
        //this.intPosition();

        this.colour = colour;
        this.width = width;
        this.height = height;
    }

    toString(){
		return this.position.toString();
    }

    // intPosition(){
	// 	this.x = Math.round(this.position.x);
	// 	this.y = Math.round(this.position.y);
	// }

	//check if the box will display on the stage
    boxOnStage(){
        if(this.world.positionOnStage(this.position.x, this.position.y)){
            return true;
        }else if(this.world.positionOnStage(this.position.x + this.width, this.position.y + this.height)){
            return true;
        }else if(this.world.positionOnStage(this.position.x + this.width, this.position.y)){
            return true;
        }else if(this.world.positionOnStage(this.position.x, this.position.y + this.height)){
            return true;
        }else{
            return false;
        }
	}
	
	//parse the box from wold to stage, return a new box
    parseBox(){
        var newBoxX = this.position.x;
        var newBoxY = this.position.y;
        var newBoxPosition = new Pair(newBoxX, newBoxY);
        var newBoxWidth = this.width;
        var newBoxHeight = this.height;
        var newBoxColour = this.colour;

		var newBox = new Box(this.world, newBoxPosition, newBoxColour, newBoxWidth, newBoxHeight);
        if(this.position.x < this.world.stage.position.x){
            if(this.position.y < this.world.stage.position.y){
                newBox.position.x = 0;
                newBox.position.y = 0;
                newBox.width = this.position.x + this.width - this.world.stage.position.x;
                newBox.height = this.position.y + this.height - this.world.stage.position.y;
            }else if(this.position.y + this.height < this.world.stage.position.y + this.world.stage.height){
                newBox.position.x = this.position.x - this.world.stage.position.x;
                newBox.position.y = this.position.y - this.world.stage.position.y;
                //newBox.width = this.position.x + this.width - this.world.stage.position.x;
                newBox.width = this.width;
            }else{
                newBox.position.x = 0;
                newBox.position.y = this.position.y - this.world.stage.position.y;
                newBox.width = this.position.x + this.width - this.world.stage.position.x;
                newBox.height = this.world.stage.position.y + this.world.stage.height - this.position.y;
            }
        }else if(this.position.x + this.width < this.world.stage.position.x + this.world.stage.width){
            if(this.position.y < this.world.stage.position.y){
                newBox.position.x = this.position.x - this.world.stage.position.x;
                newBox.position.y = 0;
                newBox.height = this.position.y + this.height - this.world.stage.position.y;
            }else if(this.position.y + this.height > this.world.stage.position.y + this.world.stage.height){
                newBox.position.x = this.position.x - this.world.stage.position.x;
                newBox.position.y = this.position.y - this.world.stage.position.y;
                newBox.height = this.world.stage.position.y + this.world.stage.height - this.position.y;
             }else{
                newBox.position.x = this.position.x - this.world.stage.position.x;
				newBox.position.y = this.position.y - this.world.stage.position.y;
            }
        }else{
            if (this.position.y < this.world.stage.position.y){
                newBox.position.x = this.position.x - this.world.stage.position.x;
                newBox.position.y = 0;
                newBox.width = this.world.stage.position.x + this.world.stage.width - this.position.x;
                newBox.height = this.position.y + this.height - this.world.stage.position.y;
            }else if (this.position.y + this.height <= this.world.stage.position.y + this.world.stage.height){
                newBox.position.x = this.position.x - this.world.stage.position.x;
                newBox.position.y = this.position.y - this.world.stage.position.y;
                newBox.width = this.world.stage.position.x + this.world.stage.width - this.position.x;
            }else{
                newBox.position.x = this.position.x - this.world.stage.position.x;
                newBox.position.y = this.position.y - this.world.stage.position.y;
                newBox.width = this.world.stage.position.x + this.world.stage.width - this.position.x;
                newBox.height = this.world.stage.position.y + this.world.stage.height - this.position.y;
            }
        }
        return newBox;
    }
    
    //check the given point is in the stage.
	positionHit(x, y){
        if(x - this.position.x < this.width && x > this.position.x){
			if (y - this.position.y < this.height && y > this.position.y){
				return true;
			} 
        }else{
            return false;
        }
    }

    isHit(){
        this.removeActor();
    }


    removeActor(){
        this.world.removeActor(this);
    }


	step(){
        return;
    }

    draw(context){
		//first check if the Box is in the stage;
		if(this.boxOnStage()){
			//the box is on the stage, initiate a new box to represent its status on stage;
            var newBox = this.parseBox();
            context.fillStyle = this.colour;
            context.fillRect(newBox.position.x, newBox.position.y, newBox.width, newBox.height);

            return;
		}else{// if it is not on the stage, do not draw it.
			return;
		}
    }


}














class AmmoBox extends Box{
    constructor(world, position, colour, width, height, ammo){
        super(world, position, colour, width, height);
        this.ammo = ammo;
    }

    removeActor(){
        this.world.player.gun.ammo += 10;
        if(this.world.player.gun.ammo > 30){
            this.world.player.gun.ammo = 30;
        }
        this.world.removeActor(this);
    }

    isHit(){
        //do nothing when been hit
        return;
    }

    draw(context){
		//first check if the Box is in the stage;
		if(this.boxOnStage()){
			//the box is on the stage, initiate a new box to represent its status on stage;
            var newBox = this.parseBox();
            context.fillStyle = this.colour;
            context.fillRect(newBox.position.x, newBox.position.y, newBox.width, newBox.height);
            context.fillStyle = "yellow";
            context.font = 'bold 17px Arial';
            context.fillText("ammo",newBox.position.x,newBox.position.y + 10);

            return;
		}else{// if it is not on the stage, do not draw it.
			return;
		}
    }
}














class Boundary extends Box{
    constructor(world, position, colour, width, height){
        super(world, position, colour, width, height);
    }

    removeActor(){
        //boundary box will not be removed
        return;
    }

    isHit(){
        this.removeActor();
    }

    boundaryOnStage(){
        if (this.world.stage.position.x < 10){
            return true;
        }else if(this.world.stage.position.y + this.world.stage.height > this.world.height - 10){
            return true;
        }else if(this.world.stage.position.y < 10){
            return true;
        }else if(this.world.stage.position.x + this.world.stage.width > this.world.width - 10){
            return true;
        }else{
            return false;
        }
    }

    draw(context){
		//first check if the Box is in the stage;
        if(this.boundaryOnStage()){
			//the box is on the stage, initiate a new box to represent its status on stage;
            var newBox = this.parseBox();
            context.fillStyle = this.colour;
            context.fillRect(newBox.position.x, newBox.position.y, newBox.width, newBox.height);
            return;
        }else{// if it is not on the stage, do not draw it.
			return;
		}
    }
}






















class EnemyAI extends Bullet{
    constructor(world, position, velocity, colour, radius){
        super(world, position, velocity, colour, radius)

    }

    positionHit(x, y){
        var xDiff = Math.abs(this.position.x - x);
        var yDiff = Math.abs(this.position.y - y);
        var centerDiff = Math.sqrt(xDiff*xDiff+yDiff*yDiff);
        if(centerDiff > this.radius){
            return false;
        }else{
            return true;
        }
    }


    hitOnBox(x, y){
        for(var i=0;i<this.world.actors.length;i++){
			if(this.world.actors[i].positionHit(x, y)){
                return true;
            }
        }
        return false;
    }

    step(){
        var target = new Pair(this.world.player.position.x, this.world.player.position.y);
        this.headTo(target);
        this.position.x=this.position.x+5*this.velocity.x;
        this.position.y=this.position.y+5*this.velocity.y;

        //if the enemy hits the player
        if(this.world.player.enemyHit(this.position.x, this.position.y, this.radius)){
            this.isHit();
            this.world.player.isHit();
        }
        
        //check if the enemy hits the box
        for(var i=0;i<this.world.actors.length;i++){
			if(this.world.actors[i].positionHit(this.position.x, this.position.y)){          
                if(this.world.actors[i] instanceof Box){//if the enemy hits a box
                    this.position.x=this.position.x-6*this.velocity.x;
                    this.position.y=this.position.y-6*this.velocity.y;
                    this.velocity.x = -this.velocity.x;
                    this.velocity.y = -this.velocity.y;
                }
            }
        }
    }

    //kill this enemy when player hits it
    isHit(){
        this.world.removeActor(this);
        this.world.player.enemyKilled += 1;
        this.world.enemyRemain -= 1;
        if(this.world.enemyRemain <= 0){
            this.world.actors = [];
            this.world.gameOver = true;
        }
    }


}






















