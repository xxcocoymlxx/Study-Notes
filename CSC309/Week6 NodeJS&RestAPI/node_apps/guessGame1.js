
// Load the http module to create an http server.
var port = 8000;
var http = require('http');
var url = require('url');

var responsesSent=0;

var secret = Math.floor((Math.random()*10 + 1));

function checkGuess(guess) {
	if (guess < secret) {
		return "too low";
	}
	if (guess > secret) {
		return "too high";
	}
	return "correct";
}

// Configure our HTTP server to respond with Hello World to all requests.
var server = http.createServer(function (request, response) {
	var headers = {"Content-Type": "text/plain"};

	//secret = Math.floor((Math.random()*10 + 1));
	// console.log(request.url);
	var params = url.parse(request.url, true).query;
	// console.log(JSON.stringify(params));
	var message = "";
	if ('guess' in params) {
		message = checkGuess(params.guess);
	}
	message += "\n";

	response.writeHead(200, headers);
	response.end(
		message, 
		function(){ responsesSent++; console.log("sent "+responsesSent+" responses"); 
	});
});

// Listen on port , IP defaults to 127.0.0.1
server.listen(port);

// Put a friendly message on the terminal
console.log("Server running at http://127.0.0.1:"+port+"/");

