/* What about serving up static content, kind of like apache? */

var port = 8000;
var express = require('express');
var app = express();

// static_files has all of statically returned content
// https://expressjs.com/en/starter/static-files.html
app.use('/zzs',express.static('static_files')); // this directory has files to be returned

app.get('/user/:id_stuff', function (req, res) {
  res.send('Returned user:'+req.params.id_stuff);
});


app.listen(port, function () {
  console.log('Example app listening on port '+port);
});

