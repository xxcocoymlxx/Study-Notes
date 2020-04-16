<?php
?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" type="text/css" href="style.css" />
		<title>Games</title>
	</head>
	<body>
		<header><h1>Game Center</h1></header>
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
		
		<h1>Personal best</h1>

		<h2>Master Mind</h2>
        <?php
	
		foreach($_SESSION['master_personal'] as $key=>$value){
			echo("<br/> $value");
		}
		?>

		<h2>Guess Game</h2>
		<?php
		foreach($_SESSION['guess_personal'] as $key=>$value){
			echo("<br/> $value");
		}
		?>
		
		<h2>15 Puzzle Game</h2>
		<?php
		foreach($_SESSION['puzzle_personal'] as $key=>$value){
			echo("<br/> $value");
		}
		?>
		
		<h2>Peg Solitare Game</h2>
		<?php
		foreach($_SESSION['peg_personal'] as $key=>$value){
			echo("<br/> $value");
		}
        ?>
        
		</main>
		<footer>
		</footer>
	</body>
</html>

