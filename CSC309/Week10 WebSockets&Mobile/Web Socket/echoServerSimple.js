// https://www.npmjs.com/package/ws
// https://github.com/websockets/ws
// https://www.espruino.com/ws

//the server

//using the library "ws", there are other socket libraries as well
var WebSocketServer = require('ws').Server
//this server will be sitting here and listening for incoming connections
   ,wss = new WebSocketServer({port: 10001});

wss.on('close', function() {
    console.log('disconnected');
});

//http://142.1.200.148:10000/echoClient.html
//when a client connect, this outer function is called
wss.on('connection', function(ws) {//this ws is an object that connects to a specific connection that is made, each of us will have a different ws object managing our connection
	//registering an event handler to this specific ws object. when you get a message, call the following function
	ws.on('message', function(message) {
		console.log(message);
		ws.send(message); 
	});
});
