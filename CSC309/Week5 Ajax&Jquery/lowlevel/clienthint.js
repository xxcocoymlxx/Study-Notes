var xmlHttp

function showHint(str) {
	if (str.length==0) { 
  		document.getElementById("txtHint").innerHTML="";
  		return;
  	}
	xmlHttp=GetXmlHttpObject();
	if (xmlHttp==null) { alert ("Your browser does not support AJAX!"); return; } 

	var url="gethint.php?q="+str+"&sid="+Math.random(); // random to prevent browser caching
	xmlHttp.onreadystatechange=stateChanged;
	xmlHttp.open("GET",url,true); // get/post, url, isAsynchronous
	xmlHttp.send(null);
} 

function stateChanged() { 
	if (xmlHttp.readyState==4) { 
		document.getElementById("txtHint").innerHTML=xmlHttp.responseText;
	}
}

function GetXmlHttpObject() {
	var xmlHttp=null;
	try { xmlHttp=new XMLHttpRequest();} // Firefox, Opera 8.0+, Safari 
	catch (e) {
		// Internet Explorer
		try { xmlHttp=new ActiveXObject("Msxml2.XMLHTTP"); }
		catch (e) { xmlHttp=new ActiveXObject("Microsoft.XMLHTTP"); }
	}
	return xmlHttp;
}
