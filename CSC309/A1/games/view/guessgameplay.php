<?php
	// So I don't have to deal with uninitialized $_REQUEST['guess']
	$_REQUEST['guess']=!empty($_REQUEST['guess']) ? $_REQUEST['guess'] : '';
?>

<!DOCTYPE html>
<html lang="en">

	<head>
		<meta charset="utf-8">
		<title>Guess Game</title>
		<link rel="stylesheet" type="text/css" href="style.css" />
	</head>

	
	<body>
		<header><h1>Guess Game</h1></header>

		<nav>
			<ul>
			<li> Games
			<li> <a href="?operation=guessgame">Guess Game</a>
			<li> <a href="?operation=15puzzles">15 Puzzles</a>
			<li> <a href="?operation=pegsolitare">Peg Solitare</a>
			<li> <a href="?operation=mastermind">Master Mind</a>
			<li> <hr>
			<li> <a href="?operation=mainpage">Main Page</a>
			<li> <a href="?operation=userprofile">User Profile</a>
			<li> <a href="?operation=gamestats">Game Stats</a>
			<li> <a href="?operation=logout">Log Out</a>
            </ul>
	</nav>

	<main>
		<?php if($_SESSION["GuessGame"]->getState()!="correct"){ ?>
			<form method="post">
				<input type="text" name="guess" value="<?php echo($_REQUEST['guess']); ?>" /> <input type="submit" name="submit" value="guess" />
			</form>
		<?php } ?>
		
		<?php echo(view_errors($errors)); ?> 

		<?php 
			foreach($_SESSION['GuessGame']->history as $key=>$value){
				echo("<br/> $value");
			}

			if($_SESSION["GuessGame"]->getState()=="correct"){ 
		?>
				<form method="post">
					<input type="submit" name="submit" value="start again" />
				</form>
		<?php 
			}
		?>
		<form method="post">
			<br><br><br>
			<a href="?operation=restart">Restart</a>
	</form>
	</main>

	<footer>
	</footer>
	</body>
</html>

