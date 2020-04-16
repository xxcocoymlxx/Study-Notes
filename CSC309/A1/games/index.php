<?php
	ini_set('display_errors', 'On');
	require_once "lib/lib.php";
	require_once "model/GuessGame.php";
	require_once "model/database.php";
	require_once "model/15puzzle.php";
	require_once "model/user.php";
	require_once "model/PegSolitare.php";
	require_once "model/MasterMind.php";

	session_save_path("sess");
	session_start(); 

	$database = new database();

	$errors=array();
	$view="";

	/* controller code */

	/* local actions, these are state transforms */
	if(!isset($_SESSION['state'])){
		$_SESSION['state']='login';
	}

	switch($_SESSION['state']){

		case "login":
			$view="login.php";

			// check if submit or not
			if(isset($_REQUEST['register']) && $_REQUEST['register']=="register"){
				$_SESSION['state']='register';
				$view="registration.php";
				break;
			} else if(empty($_REQUEST['submit']) || $_REQUEST['submit']!="login"){
				break;
			} 

			// validate and set errors
			if(empty($_REQUEST['user']))$errors[]='user is required';
			if(empty($_REQUEST['password']))$errors[]='password is required';
			if(!empty($errors))break;

			// perform operation, switching state and view if necessary
			if(!$database->dbconn){
				$errors[]="Can't connect to db";
				break;
			}

			if ($database->registeredUser($_REQUEST['user'],$_REQUEST['password'])){
				$info = $database->getUserInfo($_REQUEST['user']);
				$gender = $info['gender'];
				$birthday = $info['birthday'];
				$gift = $info['gift'];
				$sub = $info['subscribe'];
				//get all the info of current user and store them in a user object
				$_SESSION['user']= new user($_REQUEST['user'],$_REQUEST['password'],$gender,$birthday,$gift,$sub);

			//gender
			if (strncmp($gender,"female",6)==0){
				$_SESSION['user']->genderflag = 1;
			}else if (strncmp($gender,"male",4)==0){
				$_SESSION['user']->genderflag = 0;
			}else {
				$_SESSION['user']->genderflag = 3;
			}

			//gift
			if ($gift=='nogift'){
				$_SESSION['user']->giftflag = 1;
			}else if ($gift=='giftcard'){
				$_SESSION['user']->giftflag = 2;
			}else if ($gift=='3sub'){
				$_SESSION['user']->giftflag = 3;
			}else if ($gift=='secret'){
				$_SESSION['user']->giftflag = 4;
			}

			//subscription
			if ($sub=='yes'){
				$_SESSION['user']->subflag = 1;
			}else{
				$_SESSION['user']->subflag = 0;
			}	

			//setting up completed
			//directing back to main page
			$_SESSION['state']='mainpage';
			$view="mainpage.php";

			} else {
				$errors[]="invalid login";
			}

			break;

		case "register":
			// the view we display by default
			$view="registration.php";

			//if already has an account
			if(isset($_REQUEST['operation']) == 'login') {
				if($_REQUEST['operation'] == 'login') {
					$_SESSION['state'] = 'login';
					$view = 'login.php';
				}
			}

			if(empty($_REQUEST['register']) || $_REQUEST['register']!="Register"){
				break;
			} 

			// perform operation, switching state and view if necessary
			if(!$database->dbconn){
				$errors[]="Can't connect to db";
				break;
			}
			
			//error checking for username
			if(empty($_REQUEST['username'])){//if it's empty
				$errors[]='user is required';
			} else if ($database->usernameExists($_REQUEST['username'])){//if it already exists in database
				$errors[]='username already exists, please choose another username';
			}else if (strlen($_REQUEST['username'])<4){
				$errors[]='username must be at least 4 characters';
			}

			if(empty($_REQUEST['psw']))$errors[]='password is required';
			if(empty($_REQUEST['psw-repeat']))$errors[]='please enter your password again';

			if ($_REQUEST['psw'] != $_REQUEST['psw-repeat']){
				$errors[]='password does not match, please re-enter your password';
			} else if (strlen($_REQUEST['psw'])<6){
				$errors[]='password must be at least 6 characters';
			}

			if(empty($_REQUEST['gender']))$errors[]='gender is required';
			if(empty($_REQUEST['birthday']))$errors[]='birthday is required';

			//if there are error msg, break
			if(!empty($errors))break;

			if (empty($_REQUEST['subscribe'])){
				$sub = 'no';
			}else{
				$sub = 'yes';
			}

			$params = array($_REQUEST['username'],
							$_REQUEST['psw'],
							$_REQUEST['gender'],
							$_REQUEST['birthday'],		
							$_REQUEST['category'],
							$sub,
						);
			
			if ($database->createNewUser($params)){			
				//redirecting back to login page
				$_SESSION['state']='login';
				$view="login.php";
			}else {
				$errors[]='unable to create new user';
			}

			//if there are error msg, break
			if(!empty($errors))break;

			break;

		//get all the info from the database and re-populate the user profile
		//now each user should have their own user object, you can get all the info from there
		case "userprofile":
			
			$view = 'userprofile.php';

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}
		
			if(isset($_REQUEST['operation']) == 'guessgame') {
				if($_REQUEST['operation'] == 'guessgame') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}
		
			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}
		
			if(isset($_REQUEST['operation']) == '15puzzles') {
				if($_REQUEST['operation'] == '15puzzles') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}
		
			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';	
					$_SESSION['pegsolitare_state']='play';		
					$view = 'pegsolitareplay.php';
				}
			}
		
			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}
		
			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';	
					$_SESSION['mastermind_state']='play';		
					$view = 'mastermindplay.php';
				}
			}
		
			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {
					$params = array($_SESSION['user']->username);
					$master_personalres = $database->GetMasterMindPersonalBest($params);
					for ($i=0; $i<sizeof($master_personalres);$i++){
						$moves = $master_personalres[$i]['moves'];
						$sec = $master_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['master_personal'][$i] =  $score_str;
					}
		
					$puzzle_personalres = $database->GetPuzzleGamePersonalBest($params);
					for ($i=0; $i<sizeof($puzzle_personalres);$i++){
						$moves = $puzzle_personalres[$i]['moves'];
						$sec = $puzzle_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['puzzle_personal'][$i] =  $score_str;
					}
		
					$guess_personalres = $database->GetGuessGamePersonalBest($params);
					for ($i=0; $i<sizeof($guess_personalres);$i++){
						$moves = $guess_personalres[$i]['moves'];
						$sec = $guess_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['guess_personal'][$i] =  $score_str;
					}
		
					$peg_personalres = $database->GetPegSolitarePersonalBest($params);
					for ($i=0; $i<sizeof($peg_personalres);$i++){
						$moves = $peg_personalres[$i]['moves'];
						$sec = $peg_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['peg_personal'][$i] =  $score_str;
					}
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}

			if(!$database->dbconn){
				$errors[]="Can't connect to db";
				break;
			}

			// Modify Values in SQL DB If Changed.
			if(isset($_POST['update'])) {

				// Sanity check
				if($_POST['psw'] == '') {
					$errors[] = 'password cannot be null';
					break;
				}else if ($_POST['psw-repeat'] == ''){
					$errors[] = 'please re-enter you password';
				}

				if($_POST['psw-repeat'] != $_POST['psw']) {
					$errors[] = 'password does not match, please re-enter your password';
					break;
				}

				//if there's updated info, put it into the database
				//we need to update and DATABASE AND THE USER OBJECT!!!!!!!
				if ($_REQUEST['psw'] != $_SESSION['user']->password){
					$pswparams = array($_REQUEST['psw'],$_SESSION['user']->username);
					if (!$database->updatePassword($pswparams)){
						$errors[] = 'failed to update user info';
					}else{
						//update the user object at the same time
						$_SESSION['user']->updatePassword($_REQUEST['psw']);
					}
				}

				//if there's updated info, put it into the database
				if (strncmp($_REQUEST['gender'],$_SESSION['user']->gender,2)!=0){
					$genderparams = array($_REQUEST['gender'],$_SESSION['user']->username);
					if (!$database->updateGender($genderparams)){
						$errors[] = 'failed to update user info';
					}else{
						if ($_REQUEST['gender']=='male'){
							//update the user object at the same time
							$_SESSION['user']->updateGender($_REQUEST['gender']);
							$_SESSION['user']->updateGenderFlag(0);
						}else if ($_REQUEST['gender']=='female'){
							$_SESSION['user']->updateGender($_REQUEST['gender']);
							$_SESSION['user']->updateGenderFlag(1);
						}else {
							$_SESSION['user']->updateGender($_REQUEST['gender']);
							$_SESSION['user']->updateGenderFlag(3);
						}
					}
				}

				//if there's updated info, put it into the database
				if ($_REQUEST['birthday'] != $_SESSION['user']->birthday){
					$bdayparams = array($_REQUEST['birthday'],$_SESSION['user']->username);
					if (!$database->updateBirthday($bdayparams)){
						$errors[] = 'failed to update user info';
					}else {
						//update the user object at the same time
						$_SESSION['user']->updateBirthday($_REQUEST['birthday']);
					}
				}

				//if there's updated info, put it into the database
				//was subscribed and wants to cancel subscription
				if (empty($_REQUEST['subscribe'])){
					//update the database
					$subparams = array("no",$_SESSION['user']->username);
					$database->updateSub($subparams);
					$_SESSION['user']->updateSubFlag(0);
					$_SESSION['user']->updateSubscribe("no");
				}else if (!empty($_REQUEST['subscribe'])){
					$subparams = array("yes",$_SESSION['user']->username);
					$database->updateSub($subparams);
					$_SESSION['user']->updateSubFlag(1);
					$_SESSION['user']->updateSubscribe("yes");
				}
			}

			break;
		
		case "mainpage":
			$view="mainpage.php";

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'guessgame') {
				if($_REQUEST['operation'] == 'guessgame') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {

			$params = array($_SESSION['user']->username);
			$master_personalres = $database->GetMasterMindPersonalBest($params);
			for ($i=0; $i<sizeof($master_personalres);$i++){
				$moves = $master_personalres[$i]['moves'];
				$sec = $master_personalres[$i]['sec'];
				$score_str = "$i) $moves guesses in $sec seconds.";
				$_SESSION['master_personal'][$i] =  $score_str;
			}

			$puzzle_personalres = $database->GetPuzzleGamePersonalBest($params);
			for ($i=0; $i<sizeof($puzzle_personalres);$i++){
				$moves = $puzzle_personalres[$i]['moves'];
				$sec = $puzzle_personalres[$i]['sec'];
				$score_str = "$i) $moves moves in $sec seconds.";
				$_SESSION['puzzle_personal'][$i] =  $score_str;
			}

			$guess_personalres = $database->GetGuessGamePersonalBest($params);
			for ($i=0; $i<sizeof($guess_personalres);$i++){
				$moves = $guess_personalres[$i]['moves'];
				$sec = $guess_personalres[$i]['sec'];
				$score_str = "$i) $moves guesses in $sec seconds.";
				$_SESSION['guess_personal'][$i] =  $score_str;
			}

			$peg_personalres = $database->GetPegSolitarePersonalBest($params);
			for ($i=0; $i<sizeof($peg_personalres);$i++){
				$moves = $peg_personalres[$i]['moves'];
				$sec = $peg_personalres[$i]['sec'];
				$score_str = "$i) $moves moves in $sec seconds.";
				$_SESSION['peg_personal'][$i] =  $score_str;
			}				
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}

			if(isset($_REQUEST['operation']) == '15puzzles') {
				if($_REQUEST['operation'] == '15puzzles') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';		
					$_SESSION['pegsolitare_state']='play';	
					$view = 'pegsolitareplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';		
					$_SESSION['mastermind_state']='play';	
					$view = 'mastermindplay.php';
				}
			}
				
			break;

		case "gamestats":

			$view="GameStats.php";

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'guessgame') {
				if($_REQUEST['operation'] == 'guessgame') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}

			if(isset($_REQUEST['operation']) == '15puzzles') {
				if($_REQUEST['operation'] == '15puzzles') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';		
					$_SESSION['pegsolitare_state']='play';	
					$view = 'pegsolitareplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';	
					$_SESSION['mastermind_state']='play';		
					$view = 'mastermindplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}



			break;

		case "guessgame":

			if(!isset($_SESSION['guessgame_state'])){
				$_SESSION['guessgame_state']='play';
			}

			$view="guessgameplay.php";


			switch($_SESSION['guessgame_state']){
				

				case "play":

					$view="guessgameplay.php";

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}

			if(isset($_REQUEST['operation']) == '15puzzles') {
				if($_REQUEST['operation'] == '15puzzles') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';		
					$_SESSION['pegsolitare_state']='play';	
					$view = 'pegsolitareplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';	
					$_SESSION['mastermind_state']='play';		
					$view = 'mastermindplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {
					$params = array($_SESSION['user']->username);
					$master_personalres = $database->GetMasterMindPersonalBest($params);
					for ($i=0; $i<sizeof($master_personalres);$i++){
						$moves = $master_personalres[$i]['moves'];
						$sec = $master_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['master_personal'][$i] =  $score_str;
					}
		
					$puzzle_personalres = $database->GetPuzzleGamePersonalBest($params);
					for ($i=0; $i<sizeof($puzzle_personalres);$i++){
						$moves = $puzzle_personalres[$i]['moves'];
						$sec = $puzzle_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['puzzle_personal'][$i] =  $score_str;
					}
		
					$guess_personalres = $database->GetGuessGamePersonalBest($params);
					for ($i=0; $i<sizeof($guess_personalres);$i++){
						$moves = $guess_personalres[$i]['moves'];
						$sec = $guess_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['guess_personal'][$i] =  $score_str;
					}
		
					$peg_personalres = $database->GetPegSolitarePersonalBest($params);
					for ($i=0; $i<sizeof($peg_personalres);$i++){
						$moves = $peg_personalres[$i]['moves'];
						$sec = $peg_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['peg_personal'][$i] =  $score_str;
					}
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}
			if(isset($_REQUEST['operation']) == 'retart') {
				if($_REQUEST['operation'] == 'restart') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}
					
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
						$_SESSION["GuessGame"]->endtime = microtime(true);
						$_SESSION["GuessGame"]->time = $_SESSION["GuessGame"]->endtime-$_SESSION["GuessGame"]->starttime;
						$_SESSION['guessgame_state']="won";
						$view="guessgamewon.php";
					}
					$_REQUEST['guess']="";
		
					break;
		
				case "won":
					$view="guessgameplay.php";

					//generate game id
					$randnum = rand(0,100000);
					$numstr = strval($randnum);//convert the number to a string
					$gameid = $_SESSION["user"]->username.$numstr;//string concatenation

					$params = array($gameid,$_SESSION["user"]->username,$_SESSION["GuessGame"]->numGuesses, (int)$_SESSION["GuessGame"]->time);
					if (!$database->GuessGameStats($params)){
						$errors[]="failed to store the game stats into database";
					}


					if(empty($_REQUEST['submit']) || ($_REQUEST['submit']!="start again")){
						
						$errors[]="Invalid request";
						$view="guessgamewon.php";

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'guessgame') {
				if($_REQUEST['operation'] == 'guessgame') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}

			if(isset($_REQUEST['operation']) == '15puzzles') {
				if($_REQUEST['operation'] == '15puzzles') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';		
					$_SESSION['pegsolitare_state']='play';	
					$view = 'pegsolitareplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';	
					$_SESSION['mastermind_state']='play';		
					$view = 'mastermindplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {
					$params = array($_SESSION['user']->username);
					$master_personalres = $database->GetMasterMindPersonalBest($params);
					for ($i=0; $i<sizeof($master_personalres);$i++){
						$moves = $master_personalres[$i]['moves'];
						$sec = $master_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['master_personal'][$i] =  $score_str;
					}
		
					$puzzle_personalres = $database->GetPuzzleGamePersonalBest($params);
					for ($i=0; $i<sizeof($puzzle_personalres);$i++){
						$moves = $puzzle_personalres[$i]['moves'];
						$sec = $puzzle_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['puzzle_personal'][$i] =  $score_str;
					}
		
					$guess_personalres = $database->GetGuessGamePersonalBest($params);
					for ($i=0; $i<sizeof($guess_personalres);$i++){
						$moves = $guess_personalres[$i]['moves'];
						$sec = $guess_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['guess_personal'][$i] =  $score_str;
					}
		
					$peg_personalres = $database->GetPegSolitarePersonalBest($params);
					for ($i=0; $i<sizeof($peg_personalres);$i++){
						$moves = $peg_personalres[$i]['moves'];
						$sec = $peg_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['peg_personal'][$i] =  $score_str;
					}
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}
					}

					// validate and set errors
					if(!empty($errors))break;

					$_SESSION["GuessGame"]=new GuessGame();
					$_SESSION['guessgame_state']="play";
					$view="guessgameplay.php";

					break;
			}
					
			break;

			
		case "15puzzles":
			$view="15puzzleplay.php";

			if(!isset($_SESSION['15puzzle_state'])){
				$_SESSION['15puzzle_state']='play';
			}

			switch($_SESSION['15puzzle_state']){
				

				case "play":
					$view="15puzzleplay.php";
					

					//board has to be an array of form : array(0=>"img3", 1=>"img5", ...)
					//at the beginning, the board is shuffle()-ed
					if(!isset($_SESSION["board"])){
						$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();					
					}

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'guessgame') {
				if($_REQUEST['operation'] == 'guessgame') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';		
					$_SESSION['pegsolitare_state']='play';	
					$view = 'pegsolitareplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';	
					$_SESSION['mastermind_state']='play';		
					$view = 'mastermindplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {
					$params = array($_SESSION['user']->username);
					$master_personalres = $database->GetMasterMindPersonalBest($params);
					for ($i=0; $i<sizeof($master_personalres);$i++){
						$moves = $master_personalres[$i]['moves'];
						$sec = $master_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['master_personal'][$i] =  $score_str;
					}
		
					$puzzle_personalres = $database->GetPuzzleGamePersonalBest($params);
					for ($i=0; $i<sizeof($puzzle_personalres);$i++){
						$moves = $puzzle_personalres[$i]['moves'];
						$sec = $puzzle_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['puzzle_personal'][$i] =  $score_str;
					}
		
					$guess_personalres = $database->GetGuessGamePersonalBest($params);
					for ($i=0; $i<sizeof($guess_personalres);$i++){
						$moves = $guess_personalres[$i]['moves'];
						$sec = $guess_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['guess_personal'][$i] =  $score_str;
					}
		
					$peg_personalres = $database->GetPegSolitarePersonalBest($params);
					for ($i=0; $i<sizeof($peg_personalres);$i++){
						$moves = $peg_personalres[$i]['moves'];
						$sec = $peg_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['peg_personal'][$i] =  $score_str;
					}
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'restart') {
				if($_REQUEST['operation'] == 'restart') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}

					if (isset($_POST['tile0'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(0,0)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					} else if (isset($_POST['tile1'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(0,1)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile2'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(0,2)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile3'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(0,3)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile4'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(1,0)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile5'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(1,1)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile6'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(1,2)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile7'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(1,3)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile8'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(2,0)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile9'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(2,1)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile10'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(2,2)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile11'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(2,3)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile12'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(3,0)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile13'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(3,1)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile14'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(3,2)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}else if (isset($_POST['tile15'])) {
						if ($_SESSION['15puzzleGame']->moveThisTile(3,3)){
							$_SESSION["board"] = $_SESSION['15puzzleGame']->getNewBoard();
						}else {
							break;
						}
					}
					

					// perform operation, switching state and view if necessary
					if($_SESSION['15puzzleGame']->isSolved()){
						$_SESSION["15puzzleGame"]->endtime = microtime(true);
						$_SESSION["15puzzleGame"]->time = $_SESSION["15puzzleGame"]->endtime-$_SESSION["15puzzleGame"]->starttime;
						//generate game id
						$randnum = rand(0,100000);
						$numstr = strval($randnum);//convert the number to a string
						$gameid = $_SESSION["user"]->username.$numstr;//string concatenation

						$params = array($gameid,$_SESSION["user"]->username,$_SESSION["15puzzleGame"]->moves, (int)$_SESSION["15puzzleGame"]->time);
						if (!$database->PuzzleGameStats($params)){
							$errors[]="failed to store the game stats into database";
						}

						$_SESSION['15puzzle_state']="won";
						$view="15puzzlewon.php";
					}

					break;
		
				case "won":
					$view="15puzzlewon.php";

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'guessgame') {
				if($_REQUEST['operation'] == 'guessgame') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}

			if(isset($_REQUEST['operation']) == '15puzzles') {
				if($_REQUEST['operation'] == '15puzzles') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';		
					$_SESSION['pegsolitare_state']='play';	
					$view = 'pegsolitareplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';	
					$_SESSION['mastermind_state']='play';		
					$view = 'mastermindplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {
					$params = array($_SESSION['user']->username);
					$master_personalres = $database->GetMasterMindPersonalBest($params);
					for ($i=0; $i<sizeof($master_personalres);$i++){
						$moves = $master_personalres[$i]['moves'];
						$sec = $master_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['master_personal'][$i] =  $score_str;
					}
		
					$puzzle_personalres = $database->GetPuzzleGamePersonalBest($params);
					for ($i=0; $i<sizeof($puzzle_personalres);$i++){
						$moves = $puzzle_personalres[$i]['moves'];
						$sec = $puzzle_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['puzzle_personal'][$i] =  $score_str;
					}
		
					$guess_personalres = $database->GetGuessGamePersonalBest($params);
					for ($i=0; $i<sizeof($guess_personalres);$i++){
						$moves = $guess_personalres[$i]['moves'];
						$sec = $guess_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['guess_personal'][$i] =  $score_str;
					}
		
					$peg_personalres = $database->GetPegSolitarePersonalBest($params);
					for ($i=0; $i<sizeof($peg_personalres);$i++){
						$moves = $peg_personalres[$i]['moves'];
						$sec = $peg_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['peg_personal'][$i] =  $score_str;
					}
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}

					if(empty($_REQUEST['submit']) || ($_REQUEST['submit']!="start again")){
						
						$errors[]="Invalid request";
						$view="guessgamewon.php";
					}

					// validate and set errors
					if(!empty($errors))break;

					$_SESSION["15puzzleGame"]=new puzzleGame();
					$_SESSION['15puzzle_state']="play";
					$view="15puzzleplay.php";

					break;
			}

			break;

		case "mastermind":
			$view="mastermindplay.php";

			if(!isset($_SESSION['mastermind_state'])){
				$_SESSION['mastermind_state']='play';
			}
			switch($_SESSION['mastermind_state']){
				case "play":
					$view="mastermindplay.php";

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'guessgame') {
				if($_REQUEST['operation'] == 'guessgame') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}

			if(isset($_REQUEST['operation']) == '15puzzles') {
				if($_REQUEST['operation'] == '15puzzles') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';	
					$_SESSION['pegsolitare_state']='play';		
					$view = 'pegsolitareplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';
					$_SESSION['mastermind_state']='play';			
					$view = 'mastermindplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {
					$params = array($_SESSION['user']->username);
					$master_personalres = $database->GetMasterMindPersonalBest($params);
					for ($i=0; $i<sizeof($master_personalres);$i++){
						$moves = $master_personalres[$i]['moves'];
						$sec = $master_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['master_personal'][$i] =  $score_str;
					}
		
					$puzzle_personalres = $database->GetPuzzleGamePersonalBest($params);
					for ($i=0; $i<sizeof($puzzle_personalres);$i++){
						$moves = $puzzle_personalres[$i]['moves'];
						$sec = $puzzle_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['puzzle_personal'][$i] =  $score_str;
					}
		
					$guess_personalres = $database->GetGuessGamePersonalBest($params);
					for ($i=0; $i<sizeof($guess_personalres);$i++){
						$moves = $guess_personalres[$i]['moves'];
						$sec = $guess_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['guess_personal'][$i] =  $score_str;
					}
		
					$peg_personalres = $database->GetPegSolitarePersonalBest($params);
					for ($i=0; $i<sizeof($peg_personalres);$i++){
						$moves = $peg_personalres[$i]['moves'];
						$sec = $peg_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['peg_personal'][$i] =  $score_str;
					}
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}
			if(isset($_REQUEST['operation']) == 'restart') {
				if($_REQUEST['operation'] == 'restart') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';
					$_SESSION['mastermind_state']='play';			
					$view = 'mastermindplay.php';
				}
			}
			
					
					if(!isset($_SESSION["MasterBoard"])){
						$_SESSION["MasterBoard"] = new MasterMind(); 				
					}


					if (isset($_POST['red'])) {
						$_SESSION["MasterBoard"]->update_history("red");
					}else if (isset($_POST['green'])) {
						$_SESSION["MasterBoard"]->update_history("green");
					}else if (isset($_POST['blue'])) {
						$_SESSION["MasterBoard"]->update_history("blue");
					}else if (isset($_POST['orange'])) {
						$_SESSION["MasterBoard"]->update_history("orange");
					}else if (isset($_POST['pink'])) {
						$_SESSION["MasterBoard"]->update_history("pink");
					}else if (isset($_POST['brown'])) {
						$_SESSION["MasterBoard"]->update_history("brown");
					}else if (isset($_POST['check'])) {
						//player has 4 inputs
						if($_SESSION["MasterBoard"]->check_input_valid()){
							//check players answers
							if ($_SESSION["MasterBoard"]->is_solved()){
								echo "you win!!!!!!!!!!!";

								$_SESSION["MasterBoard"]->endtime = microtime(true);
								$_SESSION["MasterBoard"]->time = $_SESSION["MasterBoard"]->endtime-$_SESSION["MasterBoard"]->starttime;
								//generate game id
								$randnum = rand(0,100000);
								$numstr = strval($randnum);//convert the number to a string
								$gameid = $_SESSION["user"]->username.$numstr;//string concatenation

								$params = array($gameid,$_SESSION["user"]->username,$_SESSION["MasterBoard"]->guessTimes, (int)$_SESSION["MasterBoard"]->time);
								if (!$database->MasterMindStats($params)){
									$errors[]="failed to store the game stats into database";
								}

							}else{
								break;
							}

						}else{
							echo "You must fill the row!";
							break;
						}

					}else if (isset($_POST['delete'])) {
						//update the model
						$_SESSION["MasterBoard"]->delete_recent_his();
						break;
					}
				case "won":



			}

			break;

		case "pegsolitare":
			$view="pegsolitareplay.php";


			if(!isset($_SESSION['pegsolitare_state'])){
				$_SESSION['pegsolitare_state']='play';
			}

			switch($_SESSION['pegsolitare_state']){
				
				case "play":
					$view="pegsolitareplay.php";

			if(isset($_REQUEST['operation']) == 'logout') {
				if($_REQUEST['operation'] == 'logout') {
					$_SESSION['state'] = 'login';
					if (!empty($_SESSION)){
					session_destroy();
					}
					$view = 'login.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'guessgame') {
				if($_REQUEST['operation'] == 'guessgame') {
					$_SESSION['GuessGame']=new GuessGame();
					$_SESSION['state'] = 'guessgame';				
					$view = 'guessgameplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mainpage') {
				if($_REQUEST['operation'] == 'mainpage') {
					$_SESSION['state'] = 'mainpage';				
					$view = 'mainpage.php';
				}
			}

			if(isset($_REQUEST['operation']) == '15puzzles') {
				if($_REQUEST['operation'] == '15puzzles') {
					$_SESSION['15puzzleGame']=new puzzleGame();
					$_SESSION['state'] = '15puzzles';
					$_SESSION['15puzzle_state'] = 'play';	
					$_SESSION["board"]=$_SESSION['15puzzleGame']->getNewBoard();		
					$view = '15puzzleplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'pegsolitare') {
				if($_REQUEST['operation'] == 'pegsolitare') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';		
					$_SESSION['pegsolitare_state']='play';	
					$view = 'pegsolitareplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'userprofile') {
				if($_REQUEST['operation'] == 'userprofile') {
					$_SESSION['state'] = 'userprofile';
					$view = 'userprofile.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'mastermind') {
				if($_REQUEST['operation'] == 'mastermind') {
					$_SESSION["MasterBoard"]=new MasterMind();
					$_SESSION['state'] = 'mastermind';	
					$_SESSION['mastermind_state']='play';		
					$view = 'mastermindplay.php';
				}
			}

			if(isset($_REQUEST['operation']) == 'gamestats') {
				if($_REQUEST['operation'] == 'gamestats') {
					$params = array($_SESSION['user']->username);
					$master_personalres = $database->GetMasterMindPersonalBest($params);
					for ($i=0; $i<sizeof($master_personalres);$i++){
						$moves = $master_personalres[$i]['moves'];
						$sec = $master_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['master_personal'][$i] =  $score_str;
					}
		
					$puzzle_personalres = $database->GetPuzzleGamePersonalBest($params);
					for ($i=0; $i<sizeof($puzzle_personalres);$i++){
						$moves = $puzzle_personalres[$i]['moves'];
						$sec = $puzzle_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['puzzle_personal'][$i] =  $score_str;
					}
		
					$guess_personalres = $database->GetGuessGamePersonalBest($params);
					for ($i=0; $i<sizeof($guess_personalres);$i++){
						$moves = $guess_personalres[$i]['moves'];
						$sec = $guess_personalres[$i]['sec'];
						$score_str = "$i) $moves guesses in $sec seconds.";
						$_SESSION['guess_personal'][$i] =  $score_str;
					}
		
					$peg_personalres = $database->GetPegSolitarePersonalBest($params);
					for ($i=0; $i<sizeof($peg_personalres);$i++){
						$moves = $peg_personalres[$i]['moves'];
						$sec = $peg_personalres[$i]['sec'];
						$score_str = "$i) $moves moves in $sec seconds.";
						$_SESSION['peg_personal'][$i] =  $score_str;
					}
					$_SESSION['state'] = 'gamestats';			
					$view = 'GameStats.php';
				}
			}
			if(isset($_REQUEST['operation']) == 'restart') {
				if($_REQUEST['operation'] == 'restart') {
					$_SESSION['pegBoard']=new pegSolitareBoard();
					$_SESSION['state'] = 'pegsolitare';		
					$_SESSION['pegsolitare_state']='play';	
					$view = 'pegsolitareplay.php';
				}
			}

					if(!isset($_SESSION["pegBoard"])){
						$_SESSION["pegBoard"] = new pegSolitareBoard(); 				
					}



					if($_SESSION["pegBoard"]->is_solved()){
						$_SESSION["pegBoard"]->endtime = microtime(true);
						$_SESSION["pegBoard"]->time = $_SESSION["pegBoard"]->endtime-$_SESSION["pegBoard"]->starttime;
						//generate game id
						$randnum = rand(0,100000);
						$numstr = strval($randnum);//convert the number to a string
						$gameid = $_SESSION["user"]->username.$numstr;//string concatenation

						$params = array($gameid,$_SESSION["user"]->username,$_SESSION["pegBoard"]->moves, (int)$_SESSION["pegBoard"]->time);

						if (!$database->PegSolitareStats($params)){
							$errors[]="failed to store the game stats into database";
						}
					}

					if (isset($_POST['b1'])) {
						$_SESSION["pegBoard"]->process_action(0);
						break;
					}else if (isset($_POST['b2'])) {
						$_SESSION["pegBoard"]->process_action(1);
						break;
					}else if (isset($_POST['b3'])) {
						$_SESSION["pegBoard"]->process_action(2);
						break;
					}else if (isset($_POST['b4'])) {
						$_SESSION["pegBoard"]->process_action(3);
						break;
					}else if (isset($_POST['b5'])) {
						$_SESSION["pegBoard"]->process_action(4);
						break;
					}else if (isset($_POST['b6'])) {
						$_SESSION["pegBoard"]->process_action(5);
						break;
					}else if (isset($_POST['b7'])) {
						$_SESSION["pegBoard"]->process_action(6);
						break;
					}else if (isset($_POST['b8'])) {
						$_SESSION["pegBoard"]->process_action(7);
						break;
					}else if (isset($_POST['b9'])) {
						$_SESSION["pegBoard"]->process_action(8);
						break;
					}else if (isset($_POST['b10'])) {
						$_SESSION["pegBoard"]->process_action(9);
						break;
					}else if (isset($_POST['b11'])) {
						$_SESSION["pegBoard"]->process_action(10);
						break;
					}else if (isset($_POST['b12'])) {
						$_SESSION["pegBoard"]->process_action(11);
						break;
					}else if (isset($_POST['b13'])) {
						$_SESSION["pegBoard"]->process_action(12);
						break;
					}
					if(isset($_REQUEST['operation']) == 'gobackGC' && $_REQUEST['operation'] == 'gobackGC') {
						$_SESSION['state'] = 'mainpage';
						unset($_SESSION['pegsolitare_state']);
						$view = 'mainpage.php';
						break;
					}


				case "won":


			}
			break;
}
	require_once "view/$view";
?>