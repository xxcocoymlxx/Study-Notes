<?php 
	session_save_path("sess");
	session_start(); // must be first thing in the php file
	session_destroy();
?> 
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>destroy session</title>
	</head>
	<body>
		<h3>Destroy Session</h3>
		All variables in your session have been destroyed.
	</body>
</html>
