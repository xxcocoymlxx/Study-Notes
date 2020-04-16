var port = 8000;
var myDatabase = {};

var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('Hello World!');
});

app.get('/users/', function (req, res) {
  res.send('Here is a list of all users');
});

app.get('/user/:id_stuff', function (req, res) {
  res.send('Returned user:'+req.params.id_stuff);
});

app.get('/user/:id/scores', function (req, res) {
  res.send('Scores for '+req.params.id);
});

app.post('/user/:id/scores/:value', function (req, res) {
  res.send('Added score for '+req.params.id);
});

app.get('/blah/*', function (req, res) {
  res.send('Hello Blah!');
});

app.get('/hello', function (req, res) {
  res.send('Its me.');
});

app.listen(port, function () {
  console.log('Example app listening on port '+port+'!');
});

