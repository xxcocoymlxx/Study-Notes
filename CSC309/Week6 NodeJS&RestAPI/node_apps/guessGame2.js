
// Load the http module to create an http server.
var port = 8000;
var http = require('http');
var url = require('url');

var responsesSent=0;

var session_count = 0;
var sessions = {};

function checkGuess(guess, secret) {
	if (guess < secret) {
		return "too low";
	}
	if (guess > secret) {
		return "too high";
	}
	return "correct";
}

function randomSecret() {
	return Math.floor((Math.random()*10 + 1));
}

// Configure our HTTP server to respond with Hello World to all requests.
var server = http.createServer(function (request, response) {
	var headers = {"Content-Type": "text/plain"};
	var session_id = "";

	// console.log(JSON.stringify(request.headers));
	if ('cookie' in request.headers) {
		session_id = request.headers.cookie;
	} else {
		session_id = session_count;
		session_count++;
		headers['Set-Cookie'] = session_id;
		sessions[session_id] = {};
		sessions[session_id].secret = randomSecret();
	}

	var params = url.parse(request.url, true).query;
	var message = "";
	if ('guess' in params) {
		var secret = sessions[session_id].secret;
		message = checkGuess(params.guess, secret);
	}
	message += "\n";

	response.writeHead(200, headers);
	response.end(
		message, 
		function(){ 
			responsesSent++; 
			// console.log("sent "+responsesSent+" responses"); 
			// console.log("sessions "+JSON.stringify(sessions)); 
	});
});

// Listen on port , IP defaults to 127.0.0.1
server.listen(port);

// Put a friendly message on the terminal
console.log("Server running at http://127.0.0.1:"+port+"/");

