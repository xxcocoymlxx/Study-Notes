<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>Guess Game</title>
	</head>
	<body>
		<h1>Welcome to GuessGame</h1>
		<?php echo(view_errors($errors)); ?>
		<?php 
			foreach($_SESSION['history'] as $key=>$value){
				echo("<br/> $value");
			}
		?>
		<form method="post">
			<input type="submit" name="submit" value="start again" />
		</form>
	</body>
</html>

