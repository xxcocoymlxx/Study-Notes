<?php
	require_once "model/GuessGame.php";

	session_save_path("sess");
	session_start(); 

	ini_set('display_errors', 'On');

	$errors=array();
	$view="";

	/* controller code */
	if(!isset($_SESSION['state'])){
		$_SESSION['state']='login';
	}

	switch($_SESSION['state']){
		case "login":
			// the view we display by default
			$view="login.php";

			// check if submit or not
			if(empty($_REQUEST['submit']) || $_REQUEST['submit']!="login"){
				break;
			}

			// validate and set errors
			if(empty($_REQUEST['user'])){
				$errors[]='user is required';
			}
			if(empty($_REQUEST['password'])){
				$errors[]='password is required';
			}
			if(!empty($errors))break;

			// perform operation, switching state and view if necessary
			if($_REQUEST['user']=="arnold" && $_REQUEST['password']=="something"){
				$_SESSION['GuessGame']=new GuessGame();
				$_SESSION['state']='play';
				$view="play.php";
			} else {
				$errors[]="invalid login";
			}
			break;

		case "play":
			// the view we display by default
			$view="play.php";

			// check if submit or not
			if(empty($_REQUEST['submit'])||$_REQUEST['submit']!="guess"){
				break;
			}

			// validate and set errors
			if(!is_numeric($_REQUEST["guess"]))$errors[]="Guess must be numeric.";
			if(!empty($errors))break;

			// perform operation, switching state and view if necessary
			$_SESSION["GuessGame"]->makeGuess($_REQUEST['guess']);
			if($_SESSION["GuessGame"]->getState()=="correct"){
				$_SESSION['state']="won";
				$view="won.php";
			}
			$_REQUEST['guess']="";

			break;

		case "won":
			// the view we display by default
			$view="play.php";

			// check if submit or not
			if(empty($_REQUEST['submit'])||$_REQUEST['submit']!="start again"){
				$errors[]="Invalid request";
				$view="won.php";
			}

			// validate and set errors
			if(!empty($errors))break;


			// perform operation, switching state and view if necessary
			$_SESSION["GuessGame"]=new GuessGame();
			$_SESSION['state']="play";
			$view="play.php";

			break;
	}
	require_once "view/view_lib.php";
	require_once "view/$view";
?>
