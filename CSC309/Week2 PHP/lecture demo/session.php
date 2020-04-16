<?php 
	session_save_path("sess");
	session_start(); // must be first thing in the php file
?> 
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>session</title>
	</head>
	<body>
		<h3>session</h3>
		The contents of your session are:
		<?php 
			foreach($_SESSION as $key=>$value){
				echo("$key => $value<br/>"); 
			}
		?>
	</body>
</html>
