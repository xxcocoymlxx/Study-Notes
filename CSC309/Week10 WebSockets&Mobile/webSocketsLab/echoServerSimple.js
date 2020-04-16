// https://www.npmjs.com/package/ws
// https://github.com/websockets/ws
// https://www.espruino.com/ws

var WebSocketServer = require('ws').Server
   ,wss = new WebSocketServer({port: 10000});

wss.on('close', function() {
    console.log('disconnected');
});

wss.on('connection', function(ws) {
	ws.on('message', function(message) {
		console.log(message);
		ws.send(message); 
	});
});
