// For a completely restful api, we would need to send some kind of authentication
// token for each request. A simple trivial one is sending the user and password.
// an alternative is to send something hashed with the user and password

//in this assignment, we are using JWT to do the authentication
var secret_token;

//function used to parse cookies
function getCookie(cname) {
	var name = cname + "=";
	var decodedCookie = decodeURIComponent(document.cookie);
	var ca = decodedCookie.split(';');
	for(var i = 0; i <ca.length; i++) {
	  var c = ca[i];
	  while (c.charAt(0) == ' ') {
		c = c.substring(1);
	  }
	  if (c.indexOf(name) == 0) {
		return c.substring(name.length, c.length);
	  }
	}
	return "";
  }

//Leaderboard shows the top 10 players and their score
function gameStatsRequest(){
	$.ajax({ 
		url: "/api/leaderBoard/topTen/",
		headers: {'Authorization': "Bearer "+secret_token},
		method: "GET",
		contentType: "application/json; charset=UTF-8",
	}).done(function(data , text_status, jqXHR){
		console.log(text_status);
		console.log(jqXHR.status);

		for (i = 1; i <= 10; i++) {
			document.getElementById("row" + (i) + "username").value = data[i][0];
			document.getElementById("row" + (i) + "").value = data[i][1];
		}
	}).fail(function(err){
		alert(JSON.stringify(err.responseJSON));
		console.log(err.status);
		console.log(JSON.stringify(err.responseJSON));
	});
}

//handles user's login request
function loginRequest(){
	var username = $("#usernameLogin").val();
	var password = $("#passwordLogin").val();
	
    if (!username) {
		$('#usernameLogin').css({"outline":"solid red", "color":"red"})
		alert("Missing username field");
	} else if (!password){
		$('#passwordLogin').css({"outline":"solid red", "color":"red"})
		alert("Missing password field");
	}else {
            $.ajax({
				url: "/api/login",
				method: "POST",
				data: JSON.stringify({
					username: username,
					password: password
				}),
				contentType: "application/json; charset=UTF-8",

			}).done(function(data, text_status, jqXHR){
				//if in this case means login successful, otherwise there's gonna be an error
				var returned = JSON.stringify(data);
				console.log(returned);
				alert("login was successful!");
				goToGamePage();
				document.cookie = "username="+username;
				secret_token = data['accessToken'];			

			}).fail(function(err){
				if (err.responseJSON.status){
					alert(err.responseJSON.status);
				}
				console.log(err.status);
				alert(JSON.stringify(err.responseJSON));
				console.log(JSON.stringify(err.responseJSON));
				$('#usernameLogin').css({"outline":"solid red"})
				$('#passwordLogin').css({"outline":"solid red"})
			});
	}
}

// handles user's registration request
function registerRequest(){
	var username = $("#username-register").val();
	var password = $("#password-register").val();
	var password_repeat = $("#password-repeat-register").val();
	var email = $("#email-register").val();
	var gender = $("#gender-register").val();
	var firstname = $("#firstname-register").val();

	var pattern = new RegExp(/^[a-zA-Z0-9]{0,20}$/);
	var emailPattern = new RegExp(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,4}$/);

	if (!username){
		$('#username-register').css({"outline":"solid red", "color":"red"});
		alert("Please enter you username");
	}else if (!firstname){
		$('#firstname-register').css({"outline":"solid red", "color":"red"});
		alert("Please enter your first name");
	}else if (!password){
		$('#password-register').css({"outline":"solid red", "color":"red"});
		alert("please enter your password");
	}else if (!password_repeat){
		$('#password-repeat-register').css({"outline":"solid red", "color":"red"});
		alert("Please repeat your password for verification");
	}else if (!gender){
		$('#gender-register').css({"outline":"solid red", "color":"red"});
		alert("Please enter your gender");
	}else if (!email){
		$('#email-register').css({"outline":"solid red", "color":"red"});
		alert("Please enter your email");
	} else {
		if (!pattern.test(username)) {
			$('#username-register').css({"outline":"solid red", "color":"red"});
			alert("alpha-numeric for username only");
		} else if (!pattern.test(firstname)) {
			$('#firstname-register').css({"outline":"solid red", "color":"red"});
			alert("alpha-numeric for your first name only");
		} else if (password.length<4){
			$('#password-register').css({"outline":"solid red", "color":"red"});
			alert("Password must be longer than 4 digits");
		}else if (!emailPattern.test(email)) {
			$('#email-register').css({"outline":"solid red", "color":"red"});
			alert("Please enter a valid email address");
		} else if (password != password_repeat){
			alert("password mismatch, please re-enter");
			$('#password-repeat-register').css({"outline":"solid red", "color":"red"});
			$('#password-register').css({"outline":"solid red", "color":"red"});
		}else {
			$.ajax({
				headers: {'Authorization': "Bearer "+secret_token},
				url: "/api/register",
				method: "POST",
				data: JSON.stringify({
					username: username,
					password: password,
					gender: gender,
					email: email,
					firstname : firstname
				}),
				contentType: "application/json; charset=UTF-8",
			}).done(function(data, text_status, jqXHR) {
				console.log(text_status);
				console.log(jqXHR.status);
				var returned = JSON.stringify(data);
				console.log(returned);
				alert("Registration was Successful!");
				goToLoginPage();
			}).fail(function(err) {
				alert("username already exists");
				console.log(err.status);
				console.log(JSON.stringify(err.responseJSON));
			});
		}
	}
}

//send a request to the server to all the all the info of the user and prefill the info to the user profile
function prefillUserProfile(){
	var username = getCookie('username');
    if (!username || username == 'undefined') {
        alert("Missing Required Information");
    } else {
            $.ajax({
				headers: {'Authorization': "Bearer "+secret_token},
				url: "/api/user/"+username,
				method: "GET",
				contentType: "application/json; charset=UTF-8",
			}).done(function(data, text_status, jqXHR) {
				console.log(text_status);
				console.log(jqXHR.status);
				var returned = JSON.stringify(data);
				console.log(returned);
				document.getElementById("username-profile").value = data["username"];
				document.getElementById("password-profile").value = data["password"];
				document.getElementById("password-repeat-profile").value = data["password"];
				document.getElementById("email-profile").value = data["email"];
				document.getElementById("gender-profile").value = data["gender"];
				document.getElementById("firstname-profile").value = data["firstname"];
			}).fail(function(err) {
				if (err.responseJSON.status){
					alert("Failed Autofill");
				}
				alert(JSON.stringify(err.responseJSON));
				console.log(err.status);
				console.log(JSON.stringify(err.responseJSON));
			});
	}
}

//update user's info and send the new info to the server
function editProfileRequest(){
	var username = document.getElementById("username-profile").value;
	var password = document.getElementById("password-profile").value;
	var password_repeat = document.getElementById("password-repeat-profile").value;
	var firstname = document.getElementById("firstname-profile").value;
	var gender = document.getElementById("gender-profile").value;
	var email = document.getElementById("email-profile").value;
	
	var pattern = new RegExp(/^[a-zA-Z0-9]{0,20}$/);
	var emailPattern = new RegExp(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,4}$/);
	if (!username){
		$('#username-profile').css({"outline":"solid red", "color":"red"});
		alert("Please enter your username");
	}else if (!password){
		$('#password-profile').css({"outline":"solid red", "color":"red"});
		alert("Please enter a password");
	}else if (!password_repeat ){
		$('#password-repeat-profile').css({"outline":"solid red", "color":"red"});
		alert("Please repeat your password for varification");
	}else if (!firstname){
		$('#firstNameProfile').css({"outline":"solid red", "color":"red"});
		alert("Please enter your first name");
	}else if (!gender){
		alert("Please enter your gender");
	}else if (!email){
		$('#emailProfile').css({"outline":"solid red", "color":"red"});
		alert("Please enter your email");
	} else {
		if (!pattern.test(firstname)) {
			$('#firstNameProfile').css({"outline":"solid red", "color":"red"});
			alert("alpha-numeric for your first name only");
		} else if (!emailPattern.test(email)) {
			$('#email-profile').css({"outline":"solid red", "color":"red"});
			alert("please enter a valid email address");
		} else if (password != password_repeat){
			$('#password-profile').css({"outline":"solid red", "color":"red"});
			$('#password-repeat-profile').css({"outline":"solid red", "color":"red"});
			alert("Password mismatch, please re-enter");
		}else {
				$.ajax({
				headers: {'Authorization': "Bearer "+secret_token},
				url: "/api/user/"+username+"/update",
				method: "PUT",
				data: JSON.stringify({
					password: password,
					firstname: firstname,
					gender: gender,
					email: email
				}),
				contentType: "application/json; charset=UTF-8",
			}).done(function(data, text_status, jqXHR) {
				console.log(text_status);
				console.log(jqXHR.status);
				var returned = JSON.stringify(data);
				console.log(returned);
				alert("profile successfully updated");
			}).fail(function(err) {
				alert("profile update failed");
				console.log(err.status);
				console.log(JSON.stringify(err.responseJSON));
			});
		}
	}
}

//handles user's request for deleting an account
function deleteAccountRequest(){
	var username = document.getElementById("username-profile").value;
	if (!username) {
		alert("Missing Required Information");
	}else{
			
    $.ajax({
		headers: {'Authorization': "Bearer "+secret_token},
				url: "/api/user/"+username+"/deleteAccount",
				method: "DELETE",
				contentType: "application/json; charset=UTF-8",
			}).done(function(data, text_status, jqXHR) {
				console.log(text_status);
				console.log(jqXHR.status);
				var returned = JSON.stringify(data);
				alert("Your account has been deleted");
				location.reload();
			}).fail(function(err) {
				console.log(err.status);
				alert(JSON.stringify(err.responseJSON));
				console.log(JSON.stringify(err.responseJSON));
			});
		}
}

//send the score of the game to the server
function saveScoreRequest(kill,damage){
	var username = getCookie('username');

    if (!username || !kill || !damage) {
        alert("Missing Required Information");
    } else {
			$.ajax({
				headers: {'Authorization': "Bearer "+secret_token},
				url: "/api/"+username+"/achievement",
				method: "PUT",
				data: JSON.stringify({
					kill: kill,
					damage: damage
				}),
				contentType: "application/json; charset=UTF-8",
			}).done(function(data, text_status, jqXHR) {
				console.log(text_status);
				console.log(jqXHR.status);
				var returned = JSON.stringify(data);
			}).fail(function(err) {
				if (err.responseJSON.status){
					alert("Failed to Update Score");
				}
				alert(JSON.stringify(err.responseJSON));
				console.log(err.status);
				console.log(JSON.stringify(err.responseJSON));
			});
	}
}

function goToLoginPage(){
	$("#ui_login").show();
	$("#canvas").hide();
	$("#ui_register").hide();
	$("#gamestats").hide();
	$("#navbar").hide();
}

function goToRegistrationPage(){
	$("#ui_register").show();
    $("#canvas").hide();
	$("#ui_login").hide();
	$("#gamestats").hide();
	$("#ui_userprofile").hide();
	$("#navbar").hide();
}

function goToGamePage(){
	$("#canvas").show();
	$("#navbar").show();
	$("#ui_login").hide();
	$("#ui_register").hide();
	$("#gamestats").hide();
	$("#ui_userprofile").hide();
}

function goToGameStatsPage(){
	$("#gamestats").show();
    $("#canvas").hide();
	$("#ui_login").hide();
	$("#ui_register").hide();
	$("#ui_userprofile").hide();
	$("#navbar").show();
}

function goToUserProfilePage(){
	$("#ui_userprofile").show();
	$("#gamestats").hide();
    $("#canvas").hide();
	$("#ui_login").hide();
	$("#ui_register").hide();
	$("#ui_register").hide();
	$("#navbar").show();
}


// This is executed when the document is ready (the DOM for this document is loaded)
//set up onload evant handler here
$(document).ready(function() {	
	// set up nav bar handler
	$('#playgameNavButton').click(function() {goToGamePage();});
	$('#userprofileNavButton').click(function() {
		prefillUserProfile();
		goToUserProfilePage();});
	$('#gamestatsNavButton').click(function() {
		gameStatsRequest();
		goToGameStatsPage();});
	$('#logoutNavButton').click(function() {
		secret_token = null;
		goToLoginPage();});

	//set up handler for login page
	$('#loginButton').click(function() {loginRequest();});
	$('#registerButton').click(function() {goToRegistrationPage();});

	//set up handler for registration page
	$('#goBackLogin').click(function() {goToLoginPage();});
	$('#registerSubmitButton').click(function() {registerRequest();});
	
	//set up handler for user profile page
	$('#updateProfileButton').click(function() {editProfileRequest();});
	$('#deleteAccountButton').click(function() {deleteAccountRequest();});
	
});
