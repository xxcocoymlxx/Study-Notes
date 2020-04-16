/* What about serving up static content, kind of like apache? */

var express = require('express');
var app = express();

// static_files has all of statically returned content
// https://expressjs.com/en/starter/static-files.html
app.use('/',express.static('static_files')); // this directory has files to be returned

app.listen(10000, function () {
  console.log('Example app listening on port 10000!');
});

