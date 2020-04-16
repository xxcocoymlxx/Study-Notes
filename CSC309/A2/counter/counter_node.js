// run counter_node.js as:
// nodejs counter_node.js PORT_NUMBER

// Exercise: Complete this so that it is a truly restful api
// 1) Make sure all routes return appropriate http error status
// 2) Complete so that delete works, add this to the front end as well
// 3) Complete so that retrieve works better on the front end
// 3) Add users and login. For a truly restful api, no sessions are allowed
//    this means that you will have to send some kind of authentication
//    token on each request requiring authentication. One example is
//    user and password on each appropriate request. Another example
//    is user and hash(user+password+request_payload), the server can verify
//    that the user is the only one that could have generated the request.

var process = require('process');

var port = parseInt(process.argv[2]);

var express = require('express');
var app = express();

// http://www.sqlitetutorial.net/sqlite-nodejs/connect/
//
const sqlite3 = require('sqlite3').verbose();

// https://scotch.io/tutorials/use-expressjs-to-get-url-and-post-parameters
var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

// http://www.sqlitetutorial.net/sqlite-nodejs/connect/
// will create the db if it does not exist
// connect to the database

//my note:
// a bug: when you execute the first query, and then perform the next query imidiatly 
// java is single threaded, you wont have the result from the first qurry yet

var db = new sqlite3.Database('db/database.db', (err) => {
	if (err) {
		console.error(err.message);
	}
	console.log('Connected to the database.');
});

// https://expressjs.com/en/starter/static-files.html
app.use(express.static('static-content')); 

//NO.1
//the get() corresponds to the request method
// retrieve all counters (idempotent)
app.get('/api/counter/', function (req, res) {
	// http://www.sqlitetutorial.net/sqlite-nodejs/query/
	let sql = 'SELECT * FROM counter ORDER BY counterName;';
	//Querying all rows with all() method
	//The all() method allows you to execute an SQL query with 
	//specified parameters and call a callback to access the 
	//rows in the result set.
	db.all(sql, [], (err, rows) => {
		var result = {};
		result["counters"] = [];
  		if (err) {
    			result["error"] = err.message;
  		} else {
			rows.forEach((row) => {
				result["counters"].push(row);
			});
		}
		res.json(result);
	});
});

// retrieve specific counter (idempotent)
app.get('/api/counter/:counterName/', function (req, res) {
	var counterName = req.params.counterName;
	console.log(counterName);

	// http://www.sqlitetutorial.net/sqlite-nodejs/query/
	let sql = 'SELECT * FROM counter WHERE counterName=?';
	db.get(sql, [counterName], (err, row) => {
		var result = {};
  		if (err) {
			// Should set res.status!!
    			result["error"] = err.message;
  		} else {
			result[counterName] = row["counterValue"];
		}
		res.json(result);
	});
});

//NO.2
//the put() corresponds to the request method
// create a new counter (idempotent)
app.put('/api/counter/:counterName/', function (req, res) {
	//get the input counter name from client's request
	var counterName = req.params.counterName;
	console.log("PUT:"+counterName);

	let sql = 'INSERT INTO counter(counterName, counterValue) VALUES (?,?);';
	//here, we don't get rows back, so we use run()
	db.run(sql, [counterName, 0], function (err){
		var result = {};
  		if (err) {

			res.status(409); 
			//add a key:value pair to the response body JSON "result"
			result["error"] = err.message;
			
  		} else {

			result[counterName] = "updated rows: "+this.changes;

		}
		console.log(JSON.stringify(result));
		res.json(result);
	});
});

//NO.3
//the post() corresponds to the request method
//update a counter (not idempotent)
app.post('/api/counter/:counterName/', function (req, res) {
	var counterName = req.params.counterName;
	var amount = req.body.amount;
	console.log("POST:"+ counterName + " " + amount);

	// http://www.sqlitetutorial.net/sqlite-nodejs/update/
	let sql = 'UPDATE counter SET counterValue=counterValue+? WHERE counterName=?;';
	db.run(sql, [amount, counterName], function (err){
		var result = {};
  		if (err) {
			res.status(404); 
    		result["error"] = err.message;
  		} else {
			if(this.changes!=1){
    			result["error"] = "Not updated";
				res.status(404);
			} else {
				result[counterName] = "updated rows: "+this.changes;
			}
		}
		res.json(result);
	});
});

// EXERCISE: delete a counter (idempotent)

app.listen(port, function () {
  	console.log('Example app listening on port '+port);
});

// db.close();
//CANNOT close the database because I still have to handle client's request 

