<?php 
	session_save_path("sess");
	session_start(); // must be first thing in the php file
	// create a session variable 'target' and initialize it to a random number 
	// between 1 and 100 (see the php rand function)

	// setup session variables
	// arrays can store anything
	if(!isset($_SESSION['things']))$_SESSION['things']=array(1,"a string", 3.143, true);
?> 

<!DOCTYPE html>
<html>
<head>
	<title>
		Guess Game
	</title>
</head>
<body>
	<h6>Welcome to guessGame</h6>
	<form action="guessGame.php">
		<label>Your guess:</label>
		<input type="text" name="yourGuess">
		<input type="submit" name="checkMyGuess">
	</form>

	<?php if (isset($_REQUEST['yourGuess'])){ ?>

			<?php $randNum=rand(); ?>

			<?php if ($randNum > $_REQUEST['yourGuess'])){ ?>
				Your guess <?php echo $_REQUEST['yourGuess']?> is too low
			<?php } else { ?>
				Your guess <?php echo $_REQUEST['yourGuess']?> is too high

			<?php
				$answer=$_REQUEST['yourGuess'];
			?>
			<?php echo $_REQUEST['yourGuess']?>
		<?php } ?>

			

</body>
</html>