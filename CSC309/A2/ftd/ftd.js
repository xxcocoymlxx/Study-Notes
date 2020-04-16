/* 
 * What about serving up static content, kind of like apache? 
 * This time, you are required to present a user and password to the login route
 * before you can read any static content.
 * 
 * Express is a routing and middleware web framework that has minimal 
 * functionality of its own: An Express application is essentially a 
 * series of middleware function calls.
 *
 * Middleware functions are functions that have access to the request 
 * object (req), the response object (res), and the next middleware 
 * function in the application’s request-response cycle. The next 
 * middleware function is commonly denoted by a variable named next().
 */

var process = require('process');
// run ftd.js as 
// nodejs ftd.js PORT_NUMBER
var port = parseInt(process.argv[2]); 
var express = require('express');
var cookieParser = require('cookie-parser')

//import JSON web token library for API authentication
const jwt = require('jsonwebtoken');
//require('dotenv').config();

var app = express();
app.use(cookieParser()); // parse cookies before processing other middleware

// http://www.sqlitetutorial.net/sqlite-nodejs/connect/
//
const sqlite3 = require('sqlite3').verbose();

// https://scotch.io/tutorials/use-expressjs-to-get-url-and-post-parameters
var bodyParser = require('body-parser');
app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

var db = new sqlite3.Database('db/database.db', (err) => {
	if (err) {
		console.error(err.message);
	}
	console.log('Connected to the database.');
});

// ----------------------------------------------------------------------------------
// BEGIN: To restrict access to / 
// ----------------------------------------------------------------------------------
var user="shuruyonghuming", password="shurumima"; // REPLACE THESE TO KEEP OTHERS OUT OF YOUR APPLICATION

var id = Math.random().toString(36).substring(2, 15) + 
	Math.random().toString(36).substring(2, 15);

app.get('/login/:user/password/:password', function (req, res) {
	if(req.params.user==user && req.params.password==password){
		res.cookie("id",id);
  		res.send("Loggedin");
	} else {
  		res.send("Login failed");
 	}
});

// This is a checkpoint before allowing access to /zzs
app.use('/', function (req, res,next) {
	if(req.cookies.id==id){
		next(); // continue processing routes
	} else {
        	res.status(403).send('Not authorized');
	}
});
// ----------------------------------------------------------------------------------
// END: To restrict access to /
// ----------------------------------------------------------------------------------

app.use('/',express.static('static_files')); // this directory has files to be returned

const UserManagement = require ('./static_files/UserManagement.js');
var dbclass = new UserManagement(db);

const User = require ('./static_files/User.js');
var curr_user = new User();

var ACCESS_TOKEN_SECRET = require('crypto').randomBytes(64).toString('hex');

//a middleware function that authenticates the JSON web token for API 
//verify that is the user is correct
function authenticateToken(req, res, next) {
    //format: Bearer Token
    const authHeader = req.headers['authorization'];
    //if there is a token, get the second parameter, which is the token
    //if there is not, the token is 'undefined'
    const token = authHeader && authHeader.split(' ')[1];
    if (token == null) return res.sendStatus(401);//Unauthorized
  
    //we have a token, verify the token 
    jwt.verify(token, ACCESS_TOKEN_SECRET, (err, user) => {
      console.log(err);
      if (err) return res.sendStatus(403);//invalid token, no access

      //we have valid token now
      //the user's info is not in the request 
      req.user = user;
      next();//move on from the middleware
    })
  }

//function used to generate JSON web tokens (which expires in 60 minutes)
//the parameter user is a JSON object that contains the username and password
function generateAccessToken(user) {
    return jwt.sign(user, ACCESS_TOKEN_SECRET, { expiresIn: '60m' })
  }

//Method use to create a new user.
app.post('/api/register', function(req, res) {
	var username = req.body.username;
	var password = req.body.password;
    var gender = req.body.gender;
    var email = req.body.email;
    var firstname = req.body.firstname;

    var pattern = new RegExp(/^[a-zA-Z0-9]{0,20}$/);
	var emailPattern = new RegExp(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,4}$/);
    let result = {};

    if (!password || !username || !gender || !email || !firstname) {
        console.log('/api/register missing requirement element');
        res.status(400).json({"error":"missing requirement element"});//BAD REQUEST
    }else if(!pattern.test(username) || !pattern.test(firstname) || !emailPattern.test(email) || password.length<4) {
        res.status(400).json({"error":"missing requirement element"});//BAD REQUEST
    }
    
    dbclass.insertUser(username, password, firstname, gender, email).then(
        () => {
            res.status(200).json(result);
        }).catch(
        (err) => {
            result["error"] = err;
            res.status(409).json(result);
    });
});


//Get user information
//has a middleware function to verify the authorization using JWT
app.get('/api/user/:username', authenticateToken, function(req, res) {
    //URL Parameters are grabbed using req.param.variable_name
    var username = req.params.username;
    console.log(username);
    if (!username) {
        console.log('GET /api/user/ missing requirement element');
        res.status(400).json({"error":"missing requirement element"});//BAD REQUEST
    }

    if (!(username == req.user.username)) return res.status(403).send();//FORBIDDEN

    let result = {};
    dbclass.getUserByUsername(username).then(
        (row) => {
            if (row) {
                result["username"] = row["username"];
                result["firstname"] = row["firstname"]
                result["password"] = row["password"];;
                result["gender"] = row["gender"];
                result["email"] = row["email"];
                console.log(result);
                res.status(200).json(result);
            } else {
                //if there is no such user, it won't return an error, just en empty row
                result["error"] = "User does not exist";
                res.status(404).json(result);//NOT FOUND
            }
        }).catch(
        (err) => {
            result['error'] = err;
            res.status(500).json(result);
        });
});

//Update user profile information
//has a middleware function to verify the authorization using JWT
app.put('/api/user/:username/update', authenticateToken, function(req, res) {
    var username = req.params.username;
    var password = req.body.password;
    var gender = req.body.gender;
    var email = req.body.email;
    var firstname = req.body.firstname;

    var pattern = new RegExp(/^[a-zA-Z0-9]{0,20}$/);
	var emailPattern = new RegExp(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,4}$/);

    if (!firstname || !username || !password || !gender || !email) {
        console.log('PUT /api/user/:username missing requirement element');
        res.status(400).json({"error":"missing requirement element"});//BAD REQUEST
    }else if(!pattern.test(username) || !pattern.test(firstname) || !emailPattern.test(email) || password.length<4) {
        res.status(400).json({"error":"invalid input"});//BAD REQUEST
    }

    if (!(username == req.user.username)) return res.status(403).send();//FORBIDDEN

    var result = {};
    return dbclass.updateUser(firstname, password, email, gender, username).then(
        ()=>{
            res.status(200).json(result);
        }).catch(
        (err)=>{
            result['error'] = err;
            res.status(403).json(result);
        }
    )
});


//Method use for user login
app.post('/api/login', function(req, res) {
    var username = req.body.username;
    var password = req.body.password;

    if (!username || !password) {
        console.log('/api/login missing requirement element');
        res.status(400).json({"error":"missing requirement element"});//BAD REQUEST
    }

    var user = {username :username};
    var result = {};

    dbclass.verification(username, password).then(
        (row) => {
            if (row) {
                curr_user.setUsername(username);
                curr_user.setPassword(password);

                //a secret token has been created based on the username of the user
                const accessToken = generateAccessToken(user);
                //everytime the user login, they get a accessToken for authentication purpose
                result['accessToken'] = accessToken;
                res.status(200).json(result);
            } else {
                //user name exists but wrong password
                result['error'] = 'Password Wrong';
                res.status(401).json(result);//Unauthorized
            }
        }).catch(
            //either "user name does not exists" or "internal server error"
            (err) => {
            console.log(err);
            result['error'] = err;
            res.status(401).json(result);//Unauthorized
        });
});

//Delete user
//has a middleware function to verify the authorization using JWT
app.delete('/api/user/:username/deleteAccount', authenticateToken, function(req, res) {
    var username = req.params.username;
    if (!(username == req.user.username)) return res.status(403).send();//FORBIDDEN

    if (!username) {
        console.log('DELETE /api/user/:username/deleteAccount: missing requirement element');
        res.status(400).json({"error":"missing requirement element"});//BAD REQUEST
    }
    var result = {};
    return dbclass.deleteUserByid(username).then(
        ()=>{
            res.status(200).json(result);
        }).catch(
        (err)=>{
            result['error'] = err;
            res.status(500).json(result);//INTERNAL SERVER ERROR
        });
});


//Return top 10 achievements
app.get('/api/leaderBoard/topTen', function(req, res) {
    let result = {};
    dbclass.getTop10Score().then(
        (rows) => {
            let count = 1;
            rows.forEach((row) => {
                result[count.toString()] = [row["username"], row["kill"]];
                count += 1;
            });
            res.status(200).json(result);
        }).catch(
        (err) => {
            result['err'] = err;
            res.status(500).json(result);
        });
});

//Save user achievement into the database
//has a middleware function to verify the authorization using JWT
app.put('/api/:username/achievement', authenticateToken, function(req, res) {
    var username = req.params.username;
    var kill = req.body.kill;
    var damage = req.body.damage;

    if (!username || !kill || !damage) {
        console.log('/api/achievement/:userid missing requirement element');
        res.status(400).json({"error":"missing requirement element"});//BAD REQUEST
    }
    if (!(username == req.user.username)) return res.status(403).send();//FORBIDDEN

    var result = {};
    dbclass.insertAchievement(username, kill, damage).then(
        (row)=>{
            console.log("upadte done");
            res.status(200).json(result);
        }).catch(
        (err)=>{
            result['error'] = err;
            res.status(403).json(result);
        })
    });

app.listen(port, function () {
  console.log('Example app listening on port '+port);
});
