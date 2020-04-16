<?php 
	#you need the actual folder "sess" to store all the session informations!
	#之前你所有那些问题，history存不进去，secret number每次都变都是因为session没有存进去！
	session_save_path("sess");#this function won't create the directory for you!

	session_start(); // must be first thing in the php file
	// create a session variable 'secretNumber' and initialize it to a random number 
	// between 1 and 100 (see the php rand function)

	if(!isset($_SESSION['secretNumber']))$_SESSION['secretNumber']=rand(0,100);
	if(!isset($_SESSION['numGuesses'])) $_SESSION['numGuesses']=0;
	if(!isset($_SESSION['history']))$_SESSION['history']=Array();
?> 

<!DOCTYPE html>
<html>

<head>
	<title>
		Guess Game
	</title>
</head>

<body>
	<h1>Welcome to guessGame</h1>
	<form action="guessGame.php">
		<label>Your guess:</label>
		<input type="text" name="yourGuess">
		<input type="submit" name="submitButton", value="check my guess">
	</form>

	<?php 
	if (!isset($guess)){
		$guess = $_REQUEST["yourGuess"];
	}

	if($guess>$_SESSION["secretNumber"]){
		$result="too high";
	} else if($guess<$_SESSION["secretNumber"]){
		$result="too low";
	} else {
		$result="correct";
		session_destroy();
	}

	
	
	if(isset($_REQUEST['submitButton'])){
		$_SESSION["numGuesses"]++;
		//string interpolation
		$_SESSION["history"][] = "Guess #$_SESSION[numGuesses] was $guess and was $result.";

	echo("<ul>");
	foreach($_SESSION["history"] as $key=>$value ){
		echo("<li> <b>$key</b> $value </li>");
	}
	echo("</ul>");

	}
	?>

	<h3>Random number generated:</h3>
	<?php echo $_SESSION['secretNumber'];?>
</body>
</html>
