<?php
function a() {echo "aaaa";};
?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<link rel="stylesheet" type="text/css" href="style.css" />
		<title>Peg Solitare Game</title>
	</head>
	
	<body bgcolor=yellow>
	<header><h1>Peg Solitare</h1></header>

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
  	<!-- row1 -->
  	<table>
		<tr>
		<form method="post" action="index.php">
			<td style="padding-left:82px"><button type="submit" name="b1" value="b1" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[0]->color; ?>;
			border: none"></button></td>
		</form>
		</tr>	
	</table>
		
	<!-- row2 -->
	<table>
		<tr>
		<form method="post" action="index.php">
			<td><button type="submit" name="b2" value="b2" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[1]->color; ?>;
			border: none"></button></td>
		</form>


		<form method="post" action="index.php">
        	<td><button type="submit" name="b3" value="b3" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[2]->color; ?>;
			border: none"></button></td>
		</form>

		<form method="post" action="index.php">
        	<td><button type="submit" name="b4" value="b4" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[3]->color; ?>;
			border: none"></button></td>
		</form>

		<form method="post" action="index.php">
        	<td><button type="submit" name="b5" value="b5" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[4]->color; ?>;
			border: none"></button></td>
		</form>
		</tr>
	</table>

	<!-- row3 -->
	<table>
		<tr>
		<form method="post" action="index.php">
        	<td style="padding-left:26px"><button type="submit" name="b6" value="b6" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[5]->color; ?>;
			border: none"></button></td>
		</form>
		
		<form method="post" action="index.php">
        	<td><button type="submit" name="b7" value="b7" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[6]->color; ?>;
			border: none"></button></td>
		</form>

		<form method="post" action="index.php">
        	<td><button type="submit" name="b8" value="b8" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[7]->color; ?>;
			border: none"></button></td>
		</form>
		</tr>
	</table>
		
	<!-- row4--> 
	<table>
		<tr>
		<form method="post" action="index.php">
			<td><button type="submit" name="b9" value="b9" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[8]->color; ?>;
			border: none"></button></td>
		</form>

		<form method="post" action="index.php">
        	<td><button type="submit" name="b10" value="b10" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[9]->color; ?>;
			border: none"></button></td>
		</form>

		<form method="post" action="index.php">
        	<td><button type="submit" name="b11" value="b11" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[10]->color; ?>;
			border: none"></button></td>
		</form>

		<form method="post" action="index.php">
        	<td><button type="submit" name="b12" value="b12" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[11]->color; ?>;
			border: none"></button></td>
		</form>
		</tr>
	</table>
		
	<!-- row5--> 
	<table>
		<tr>
		<form method="post" action="index.php">    
        	<td style="padding-left:82px"><button type="submit" name="b13" value="b13" 
			style="width: 50px; height: 50px; border-radius:50%;background-color:<?php echo $_SESSION["pegBoard"]->allPieces[12]->color; ?>;
			border: none"></button></td>
		</form>
      	</tr>
	</table>
	<form method="post">
			<br><br><br>
			<a href="?operation=restart">Restart</a>
	</form>

	</main>

	<footer>
	</footer>
    </body>
</html>