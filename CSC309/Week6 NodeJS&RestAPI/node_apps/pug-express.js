var port = 8000;
var express = require('express');
var app = express();

app.get('/testpug', function (req, res) {
  res.render('test.pug', { title: 'Hey', message: 'Hello there!'});
});

app.listen(port, function () {
  console.log('Example app listening on port '+port+'!');
});

