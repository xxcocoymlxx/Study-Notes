




		// ws.send(message); 
		console.log(message);
		messages.push(message);
		ws.send(message); 
		ws.send(messages[i]);
		wss.broadcast(message);
	// Alternatively
	// this.clients.forEach(function (ws){ ws.send(message); });
	for(i=0;i<messages.length;i++){
	for(let ws of this.clients){ 
	var i;
	ws.on('message', function(message) {
	}
	}
	});
    console.log('disconnected');
   ,wss = new WebSocketServer({port: 10000});
var WebSocketServer = require('ws').Server
var messages=[];
wss.broadcast = function(message){
wss.on('close', function() {
wss.on('connection', function(ws) {
}
});
});
