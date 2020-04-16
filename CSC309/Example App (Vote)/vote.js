require('./static-content/lib/constants.js'); // defines wwPort and wwWsPort

var express = require('express');
var app = express();
var votes = { yes:0 , no:0 } ;
// Web sockets to broadcast results

var WebSocketServer = require('ws').Server
   ,wss = new WebSocketServer({port: wwWsPort});

wss.on('close', function() {
    console.log('disconnected');
});

wss.broadcast = function(){
        for(let ws of this.clients){
                ws.send(JSON.stringify(votes));
        }
}

wss.on('connection', function(ws) {
        ws.send(JSON.stringify(votes));
});


var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

// https://expressjs.com/en/starter/static-files.html
app.use(express.static('static-content')); 

app.put('/api/vote/:value/', function (req, res) {
	var voteValue = req.params.value;
	if(voteValue=="yes")votes.yes++;
	if(voteValue=="no")votes.no++;
	
	console.log("PUT:"+voteValue);
	console.log("Total Votes so far:"+votes);
	var result = { result: "ok" , currentVotes: votes};
	console.log(JSON.stringify(result));
	res.json(result);
	wss.broadcast();
});

app.listen(wwPort, function () {
  	console.log('Example app listening on port '+wwPort);
});

