<?php 
	session_save_path("sess");
	session_start(); // must be first thing in the php file
	// good idea to initialize/load all session variables used in this page in one place
	if(!isset($_SESSION['total']))$_SESSION['total']=0;
?> 
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>addit05</title>
	</head>
	<body>
		<h3>Sessions</h3>
		<form> 
			<input size="2" type="text" name="num"/>
			<input type="submit" name="whichSubmit" value="add to running total" />
		</form>
		<?php 
			if(isset($_REQUEST['num'])){
				$_SESSION['total']=$_SESSION['total']+$_REQUEST['num'];
			}
		?>
		<h3>The Total So Far</h3>
		<?php echo $_SESSION['total'] ?>
		<h3>Actions</h3>
		<a href="destroySession.php">Destroy Session</a>
		
		<p>
			<b>Note:</b> You can also unset particular session variables <b>Example:</b>
<xmp>
unset($_SESSION('total')); 
</xmp>
		</p>

		<h3>Exercises</h3>
		<ul>
		<li> Modify this so that it also keeps track of the number of visits you have made to this page.
			<b>Hint:</b> Add a 'visitCount' to the $_SESSION.
		</li> 
		<li> Modify this so that it tracks the largest and smallest numbers added.  </li> 
		<li> Create a <a href="guess.php">number guessing game</a>.  </li> 
		</ul>
	</body>
</html>
