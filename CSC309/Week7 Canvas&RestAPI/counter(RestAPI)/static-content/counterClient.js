// See the JQuery documentation at ... 
// http://api.jquery.com/
// http://learn.jquery.com/
// See my JQuery and Ajax notes 
// Could also use the fetch api see...
// https://www.sitepoint.com/xmlhttprequest-vs-the-fetch-api-whats-best-for-ajax-in-2019/

function login(){
	// Normally would check the server to see if the credentials checkout
	$("#ui_login").hide();
	$("#ui_counter").show();
}

// Request all counters from the server
function retrieveAll(){
	// For a completely restful api, we would need to send some kind of authentication
	// token for each request. A simple trivial one is sending the user and password
	// an alternative is to send something hashed with the user and password

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

// add a counter new counter
function create(){
	$.ajax({ 
		method: "POST", 
		url: "/api/counter/"+$("#createCounterName").val()
	}).done(function(data){
		console.log("Got back:"+JSON.stringify(data));
		if("error" in data){ console.log(data["error"]); }
		else { retrieveAll(); }
	});
}

// increment a counter
function update(){
	$.ajax({ 
		method: "PUT", 
		url: "/api/counter/"+$("#updateCounterName").val()+"/", 
		data: { amount: $("#updateCounterAmount").val() }
	}).done(function(data, text_status, jqXHR){
		console.log(JSON.stringify(data));
		console.log(text_status);
		console.log(jqXHR.status);
		retrieveAll();
	}).fail(function(err){
		console.log(err.status);
		console.log(JSON.stringify(err.responseJSON));
	});
}


// This is executed when the document is ready (the DOM for this document is loaded)
$(function(){
	// Setup all events here and display the appropriate UI
	$("#loginSubmit").on('click',function(){ login(); });
	$("#createCounterSubmit").on('click',function(){ create(); });
	$("#updateCounterSubmit").on('click',function(){ update(); });
	$("#ui_login").show();
	$("#ui_counter").hide();
});
