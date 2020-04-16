//express and websocket all in one (unlike express_static.js and echoServerSimple.js)
//go to : http://localhost:10000/echoClient.html

//the underlying technology for web socket is still http
//it actually makes a http connection first and upgrades it to a socket connection
var staticPort = 10000;
var webSocketPort = staticPort+1;

var express = require('express');
var app = express();


// static_files has all of statically returned content
// https://expressjs.com/en/starter/static-files.html
app.use('/',express.static('static_files')); // this directory has files to be returned

app.listen(staticPort, function () {
  console.log('Static content on port:'+staticPort);
});

// Web Sockets
var WebSocketServer = require('ws').Server
   ,wss = new WebSocketServer({port: webSocketPort});

var messages=[];

wss.on('close', function() {
    console.log('disconnected');
});

wss.broadcast = function(message){
	for(let ws of this.clients){ 
		ws.send(message); 
	}

	// Alternatively
	// this.clients.forEach(function (ws){ ws.send(message); });
}

wss.on('connection', function(ws) {
	var i;
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
