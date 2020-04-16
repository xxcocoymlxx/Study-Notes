<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" type="text/css" href="style.css" />
		<title>15 Puzzles</title>
    </head>
    
<body bgcolor=white>
<header><h1>15 Puzzle Game</h1></header>


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
<center>
<?php if(! ($_SESSION["15puzzleGame"]->isSolved())){ ?>
<table>
<tr>
	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile0" value="someValue"><img src="<?php echo $_SESSION["board"][0]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile1" value="someValue"><img src="<?php echo $_SESSION["board"][1]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile2" value="someValue"><img src="<?php echo $_SESSION["board"][2]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile3" value="someValue"><img src="<?php echo $_SESSION["board"][3]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

</tr>

<tr>
<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile4" value="someValue"><img src="<?php echo $_SESSION["board"][4]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile5" value="someValue"><img src="<?php echo $_SESSION["board"][5]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile6" value="someValue"><img src="<?php echo $_SESSION["board"][6]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile7" value="someValue"><img src="<?php echo $_SESSION["board"][7]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

</tr>


<tr>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile8" value="someValue"><img src="<?php echo $_SESSION["board"][8]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile9" value="someValue"><img src="<?php echo $_SESSION["board"][9]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile10" value="someValue"><img src="<?php echo $_SESSION["board"][10]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile11" value="someValue"><img src="<?php echo $_SESSION["board"][11]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

</tr>
<tr>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile12" value="someValue"><img src="<?php echo $_SESSION["board"][12]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile13" value="someValue"><img src="<?php echo $_SESSION["board"][13]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile14" value="someValue"><img src="<?php echo $_SESSION["board"][14]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

	<td>
	<form method="post" action="index.php">
	<button type="submit" name="tile15" value="someValue"><img src="<?php echo $_SESSION["board"][15]; ?>" alt="SomeAlternateText"></button>
	</form >
	</td>

</tr>
</table>
<form method="post">
			<br><br><br>
			<a href="?operation=restart">Restart</a>
	</form>
<?php } ?>

</center>
</main>

<footer>
</footer>

</body>
</html>
