world=null;
view = null;
interval=null;

function setupGame(){
	world=new World(document.getElementById('stage'));

	// https://javascript.info/keyboard-events
	// document.addEventListener('keydown', moveByKey);
	// document.addEventListener('keyup', moveByKey);
	window.addEventListener('keydown', function (e) {
		world.keys = (world.keys || []);
		world.keys[e.keyCode] = true;
	})
	window.addEventListener('keyup', function (e) {
		world.keys[e.keyCode] = false;
	})

	window.addEventListener('mousemove', function (e) {
		
		world.player.parseGunPosition(e.pageX, e.pageY);
		world.mouseClickX = e.pageX;
		world.mouseClickY = e.pageY;
		console.log(e.pageX);
		console.log(e.pageY);		
	})
	window.addEventListener('mousedown', function (e) {
		world.mouseClick = true;
	})
	window.addEventListener('mouseup', function (e) {
		clearInterval(world.timer);
		world.mouseClick = false;
	})

	return world;
}

function startGame(){
	interval=setInterval(function(){ world.step(); world.draw(); },20);
}

function pauseGame(){
	clearInterval(interval);
	interval=null;
}

