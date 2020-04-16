var port = 8000;
// Load the http module to create an http server.
var http = require('http');

var responsesSent=0;

// Configure our HTTP server to respond with Hello World to all requests.
var server = http.createServer(function (request, response) {
	console.log(request);
	response.writeHead(200, {"Content-Type": "text/plain"});
	response.end("Hello World\n", function(){ 
		responsesSent++; 
		console.log("sent "+responsesSent+" responses");
	});
});

// Listen on port port, IP defaults to 127.0.0.1
server.listen(port);

// Put a friendly message on the terminal
console.log("Server running at http://127.0.0.1:"+port+"/");

