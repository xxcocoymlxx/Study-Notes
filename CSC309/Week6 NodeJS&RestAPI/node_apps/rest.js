// https://restfulapi.net/http-methods/
// https://restfulapi.net/http-status-codes/
var port = 8000;
var collection = {};
var maxId = 0;

var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('Hello World!');
});

app.get('/collection/', function (req, res) {
  res.statusCode = 200;
  res.json(collection);
});

app.get('/collection/:key', function (req, res) {
  var key = req.params.key;
  if(key in collection){
	var reply = {};
	reply[key]=collection[key];
  	res.statusCode = 200;
  	res.json(reply);
  } else {
	// There is a debate on whether this should be 204 or 404!
  	res.statusCode = 404;
  	res.send('');
  }
});

app.put('/collection/:key/:value', function (req, res) {
  var key = req.params.key;
  var value = req.params.value;
  if(key in collection){
  	res.statusCode = 204;
  } else {
	// Can send back the location of the new resource
  	res.statusCode = 201;
  }
  collection[key]=value;
  res.send('');
});

app.listen(port, function () {
  console.log('Example app listening on port '+port+'!');
});

