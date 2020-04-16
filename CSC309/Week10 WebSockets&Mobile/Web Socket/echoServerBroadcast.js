//how to run this:
// 1. node express-static.js
// 2. node echoServerBroadcast.js
// 3. http://localhost:10000/echoClient.html


var WebSocketServer = require('ws').Server
   ,wss = new WebSocketServer({port: 10001});

var messages=[];//storing all the messages locally

wss.on('close', function() {
    console.log('disconnected');
});


//added a new broadcast method to this websocket object
wss.broadcast = function(message){
	for(let ws of this.clients){ 
		ws.send(message); 
	}

	// Alternatively
	// this.clients.forEach(function (ws){ ws.send(message); });
}

//when you first get a connection
wss.on('connection', function(ws) {
	var i;
	//show all the messages on the screen
	for(i=0;i<messages.length;i++){
		ws.send(messages[i]);
	}
	ws.on('message', function(message) {
		console.log(message);
		// ws.send(message); 
		wss.broadcast(message);
		messages.push(message);
	});
});


//A3 heads up: send the whole world to the client, not just messages