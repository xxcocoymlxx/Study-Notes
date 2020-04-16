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
		<?php echo(view_errors($errors)); ?>
		<?php 
			foreach($_SESSION['GuessGame']->history as $key=>$value){
				echo("<br/> $value");
			}
		?>
		<form method="post">
			<input type="submit" name="submit" value="start again" />
		</form>

		</main>

		<footer>
		</footer>
	</body>
</html>

