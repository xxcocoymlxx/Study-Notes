<?php
	ini_set('display_errors', 'On');
	session_save_path("sess");
	session_start(); 

	require_once "model/model.php";

	$errors=array();
	$view="";

	/* controller code */
	if(!isset($_SESSION['state'])){
		$_SESSION['state']='start';
	}

	switch($_SESSION['state']){
		case "start":
			$view="login.php";
			$_SESSION['state']='login';
			break;

		case "login":
			// the view we display by default
			$view="login.php";

			// check parameters
			if(empty($_REQUEST['submit']))break;
			if(empty($_REQUEST['user']))$errors[]='user is required';
			if(empty($_REQUEST['password']))$errors[]='password is required';
			if(!empty($errors))break;

			// perform operation, switching state and view if necessary
			if($_REQUEST['user']=="arnold" && $_REQUEST['password']=="something"){
				start_game();
				$_SESSION['state']='play';
				$view="play.php";
			} else {
				$errors[]="invalid login";
			}
			break;

		case "play":
			// the view we display by default
			$view="play.php";

			// check parameters
			if(empty($_REQUEST['submit'])){
				break;
			}
			if($_REQUEST['submit']!="guess"){
				$errors[]="Invalid request";
				break;
			}
			if(!is_numeric($_REQUEST["guess"])){
				$errors[]="Guess must be numeric.";
				break;
			}

			// perform operation, switching state and view if necessary
			if(make_guess($_REQUEST['guess'])=="correct"){
				$_SESSION['state']="won";
				$view="won.php";
			}
			$_REQUEST['guess']="";

			break;

		case "won":
			// the view we display by default
			$view="play.php";

			// check parameters
			if(empty($_REQUEST['submit'])||$_REQUEST['submit']!="start again"){
				$errors[]="Invalid request";
				$view="won.php";
			}
			if(!empty($errors))break;

			// perform operation, switching state and view if necessary
			start_game();
			$_SESSION['state']="play";
			$view="play.php";

			break;
	}

	require_once "view/view_lib.php";
	require_once "view/$view";
?>


