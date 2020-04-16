<?php 
	session_save_path("sess");
	session_start(); // must be first thing in the php file
	// create a session variable 'target' and initialize it to a random number 
	// between 1 and 100 (see the php rand function)
?> 
<html>
	<body>
		<h3>Guess the number</h3>
		<form> 
			<input size="2" type="text" name="guess"/>
			<input type="submit" name="whichSubmit" value="submit" />
		</form>
		<?php 
			// if the user submitted the guess
			// 	determine if the guess is high, low or correct
			// 	if it is correct print out 'you got it' and 
			//	either destroy the session or unset the appropriate
			//	session variables (ie unset($_SESSION('total'))
		?>
		<h3>Additional Exercises</h3>
		<ul>
		<li> Keep track of the number of guesses</li>
		</ul>
	</body>
</html>
