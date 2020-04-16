// See the JQuery documentation at ... 
// http://api.jquery.com/
// http://learn.jquery.com/
// See my JQuery and Ajax notes 

function login(){
	// Normally would check the server to see if the credentials checkout
	$("#ui_login").hide();
	$("#ui_counter").show();
}

	/*
	a useful tut: http://tutorials.jenkov.com/jquery/ajax.html
	
	First the $.ajax() function is called. This function is passed a JSON which 
	contains information about the AJAX request to make.
	The $.ajax() function returns an object. On this object the example calls 
	three functions: done(), fail() and always().

	1. The done() function is given a function as parameter. The callback function 
	passed as parameter to the done() function is executed if the AJAX request succeeds.

	2. The fail() is also given a function as parameter. The callback function passed as
	parameter to the fail() function is called if the AJAX request fails. 

	3. The callback function passed to the always() function is called whenever the 
	AJAX request finishes, regardless of whether or not the AJAX request succeeds or fails. 
	*/
	
// Request all counters from the server
function retrieveAll(){
	// For a completely restful api, we would need to send some kind of authentication
	// token for each request. A simple trivial one is sending the user and password.
	// an alternative is to send something hashed with the user and password

	//NO.1
	//对应counter_node里的NO.1
	$.ajax({ 
		method: "GET", 
		url: "/api/counter/"
	}).done(function(data){
		console.log(JSON.stringify(data));
		var allCounters = "";
		for(i=0;i<data["counters"].length;i++){
			allCounters += "<br/>"+data["counters"][i].counterName+" "+data["counters"][i].counterValue;
		}
		$("#allCounters").html(allCounters);
	});
}

//NO.2
// add a counter new counter
function create(){
	$.ajax({ 
		method: "PUT", 
		//get the field "createCounterName" from index.html
		url: "/api/counter/"+$("#createCounterName").val()
	}).done(function(data){
		console.log("Got back:"+JSON.stringify(data));
		if("error" in data){ console.log(data["error"]); }
		else { retrieveAll(); }//send another request to get all the counters
	});
}

//NO.3
//increment a counter
function update(){
	$.ajax({ 
		method: "POST", 
		url: "/api/counter/"+$("#updateCounterName").val()+"/", 
		data: { amount: $("#updateCounterAmount").val() }
		//the data is in the request BODY
	}).done(function(data, text_status, jqXHR){
		//these values are not printed in our terminal
		//only the client side console.log() are printed in our terminal

		//these print statements are printed in "developer tools" 
		console.log(JSON.stringify(data));//{"AnotherCounter":"updated rows: 1"}
		console.log(text_status);//success
		console.log(jqXHR.status);//200
		retrieveAll();//get another AJAX request and print all counters
	}).fail(function(err){
		console.log(err.status);
		console.log(JSON.stringify(err.responseJSON));
	});
}


// This is executed when the document is ready (the DOM for this document is loaded)
//set up onload evant handler here
$(function(){
	// Setup all events here and display the appropriate UI
	$("#loginSubmit").on('click',function(){ login(); });

	//the log in swtiches the ui_login and ui_counter
	$("#createCounterSubmit").on('click',function(){ create(); });
	$("#updateCounterSubmit").on('click',function(){ update(); });
	$("#ui_login").show(); //show this onw
	$("#ui_counter").hide(); // hide the div
});
