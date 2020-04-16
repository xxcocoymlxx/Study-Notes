<?php
// So I don't have to deal with unset $_REQUEST['user'] when refilling the form
$_REQUEST['user']=!empty($_REQUEST['user']) ? $_REQUEST['user'] : '';
$_REQUEST['password']=!empty($_REQUEST['password']) ? $_REQUEST['password'] : '';
?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>Guess Game</title>
	</head>
	<body>
		<h1>Welcome to GuessGame</h1>
		<form method="post">
			<table>
				<!-- Trick below to re-fill the user form field -->
				<tr><th style="text-align:right;">User:</th><td><input type="text" name="user" value="<?php echo($_REQUEST['user']); ?>" /></td></tr>
				<tr><th style="text-align:right;">Password:</th><td> <input type="password" name="password" /></td></tr>
				<tr><th>&nbsp;</th><td><input type="submit" name="submit" value="login" /></td></tr>
				<tr><th>&nbsp;</th><td><?php echo(view_errors($errors)); ?></td></tr>
			</table>
		</form>
	</body>
</html>

