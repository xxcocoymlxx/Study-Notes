// Load the http module to create an http server.
var port = 8000;
var http = require('http');
var url = require('url');

var responsesSent=0;
var secret = 5;

function checkNumber(guess){
	if(guess<secret)return "small";
	if(guess>secret)return "large";
	if(guess==secret)return "correct";
	return "";
}

// Configure our HTTP server to respond with Hello World to all requests.
var server = http.createServer(function (request, response) {
	var headers = {"Content-Type": "text/plain"};
 	var params = url.parse(request.url, true).query;
	var message="";

	if('guess' in params){
		message = checkNumber(params.guess);
	}
	message +="\n";
	// message += JSON.stringify(request.headers)+'\n';
	// message += request.url;

	response.writeHead(200, headers);
	response.end(
		message, 
		function(){ responsesSent++; console.log("sent "+responsesSent+" responses"); 
	});
});

// Listen on port port, IP defaults to 127.0.0.1
server.listen(port);

// Put a friendly message on the terminal
console.log("Server running at http://127.0.0.1:"+port+"/");

