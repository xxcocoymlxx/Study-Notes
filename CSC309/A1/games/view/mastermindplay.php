<?php
	// So I don't have to deal with uninitialized $_REQUEST['guess']
	$_REQUEST['guess']=!empty($_REQUEST['guess']) ? $_REQUEST['guess'] : '';
?>

<!DOCTYPE html>
<html lang="en">

	<head>
		<meta charset="utf-8">
		<title>Master Mind</title>
		<link rel="stylesheet" type="text/css" href="style.css" />
	</head>

	
	<body bgcolor=#47C4ED>

	<header><h1>Master Mind Game</h1></header>
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
         <!-- table for color selection buttons -->
        <table border="1" width="120px" height="auto">
		<tr>
        <form method="post" action="index.php">
        	<td><button type="submit" name="red" value="red" 
			style="width: 10px; height: 10px; border-radius:50%;background-color:red;
			border: none"></button></td>
		</form>

        <form method="post" action="index.php">
        	<td><button type="submit" name="green" value="green" 
			style="width: 10px; height: 10px; border-radius:50%;background-color:green;
			border: none"></button></td>
		</form>

        <form method="post" action="index.php">
        	<td><button type="submit" name="blue" value="blue" 
			style="width: 10px; height: 10px; border-radius:50%;background-color:blue;
			border: none"></button></td>
		</form>

        <form method="post" action="index.php">
        	<td><button type="submit" name="orange" value="orange" 
			style="width: 10px; height: 10px; border-radius:50%;background-color:orange;
			border: none"></button></td>
		</form>

        <form method="post" action="index.php">
        	<td><button type="submit" name="pink" value="pink" 
			style="width: 10px; height: 10px; border-radius:50%;background-color:pink;
			border: none"></button></td>
		</form>

        <form method="post" action="index.php">
        	<td><button type="submit" name="brown" value="brown" 
			style="width: 10px; height: 10px; border-radius:50%;background-color:brown;
			border: none"></button></td>
		</form>

        </tr>
		
	    </table>

		<div>
		<!-- add "delete" and "check" button -->
		<form method="post">
					<input type="submit" name="check" value="check" />
		</form>

		<form method="post">
					<input type="submit" name="delete" value="delete" />
		</form>
		</div>

        <!-- table for color selection buttons ends -->
		<!-------------------------------------------------------------------------------------->

		<center>
		<?php  for ($i = 0; $i < 10; $i++){ ?>
        <!-- table for displaying guesses and feedback ends -->
        <table border="1" width="150px" height="auto"> 
            <tr>
            <!-- the 2nd table: 4 buttons for displaying user's guesses -->
            <td>
            <button type="submit" name="b1" value="black" 
			style="width: 20px; height: 20px; 
			border-radius:50%;background-color:<?php echo $_SESSION["MasterBoard"]->playerHistory[$i][0]; ?>;
			border: none"></button>

            <button type="submit" name="b2" value="black" 
			style="width: 20px; height: 20px; 
			border-radius:50%;background-color:<?php echo $_SESSION["MasterBoard"]->playerHistory[$i][1]; ?>;
			border: none"></button>

            <button type="submit" name="b3" value="black" 
			style="width: 20px; height: 20px; 
			border-radius:50%;background-color:<?php echo $_SESSION["MasterBoard"]->playerHistory[$i][2]; ?>;
			border: none"></button>

            <button type="submit" name="b4" value="black" 
			style="width: 20px; height: 20px; 
			border-radius:50%;background-color:<?php echo $_SESSION["MasterBoard"]->playerHistory[$i][3]; ?>;
			border: none"></button>
            </td>

			<!-- first feedback button -->
            <td>
			<table>
				<tr>
					<td>
            			<form method="post" action="index.php">
        					<button type="submit" name="f1" value="black" 
							style="width: 10px; height: 10px; border-radius:50%;
							background-color:<?php echo $_SESSION["MasterBoard"]->feedbacks[$i][0]; ?>;
						border: none"></button>
		    			</form>
					</td>

					<td>
            		<!-- second feedback button in first row-->
            			<form method="post" action="index.php">
        				<button type="submit" name="f2" value="black" 
						style="width: 10px; height: 10px; border-radius:50%;
						background-color:<?php echo $_SESSION["MasterBoard"]->feedbacks[$i][1]; ?>;
						border: none"></button>
		    			</form>
            		</td>
            	</tr>

            	<tr>
            		<!-- first feedback button in 2nd row -->
            		<td>
            			<form method="post" action="index.php">
        				<button type="submit" name="f3" value="black" 
						style="width: 10px; height: 10px; border-radius:50%;
						background-color:<?php echo $_SESSION["MasterBoard"]->feedbacks[$i][2]; ?>;
						border: none"></button>
		    			</form>
					</td>

					<td>
           				 <!-- second feedback button in 2nd row-->
           				 <form method="post" action="index.php">
        				<button type="submit" name="f4" value="black" 
						style="width: 10px; height: 10px; border-radius:50%;
						background-color:<?php echo $_SESSION["MasterBoard"]->feedbacks[$i][3]; ?>;
						border: none"></button>
		    			</form>
            		</td>
            	</tr> 
			</table> 
			</td>

            </tr>
		</table>
		<br>

		<?php } ?>

		<table border="1" width="150px" height="auto"> 
			Solution:
            <tr>
            <!-- the 2nd table: 4 buttons for displaying user's guesses -->
            <td>
            <button type="submit" name="b1" value="black" 
			style="width: 20px; height: 20px; 
			border-radius:50%;background-color:<?php echo $_SESSION["MasterBoard"]->result[0]; ?>;
			border: none"></button>

            <button type="submit" name="b2" value="black" 
			style="width: 20px; height: 20px; 
			border-radius:50%;background-color:<?php echo $_SESSION["MasterBoard"]->result[1]; ?>;
			border: none"></button>

            <button type="submit" name="b3" value="black" 
			style="width: 20px; height: 20px; 
			border-radius:50%;background-color:<?php echo $_SESSION["MasterBoard"]->result[2]; ?>;
			border: none"></button>

            <button type="submit" name="b4" value="black" 
			style="width: 20px; height: 20px; 
			border-radius:50%;background-color:<?php echo $_SESSION["MasterBoard"]->result[3]; ?>;
			border: none"></button>
            </td>
		</table>
		<form method="post">
			<br><br><br>
			<a href="?operation=restart">Restart</a>
		</form>
		</center>

        

        <!-- table for displaying guesses and feedback ends -->
		
		<?php echo(view_errors($errors)); ?> 

	</main>

	<footer>
	</footer>
	
	</body>
</html>

