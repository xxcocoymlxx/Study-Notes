<?php
	header('Content-Type: application/json');
	session_save_path("sess");
	session_start();
	if(!isset($_SESSION['secret'])){
		$_SESSION['secret']=rand(1,10);
	}
	
	$reply=array();
	$reply["error_message"]="";

        /** check for authorization **/
	/**
        if(!is_authorized()){
                $reply["error_message"]="Access denied";
                goto leave;
        }
	**/

	/** default state change **/

	/** check transport **/
	if(!isset($_REQUEST['request'])){
		$reply["error_message"]="Invalid request. No request sent.";
		goto leave;
	}
	$request=json_decode($_REQUEST['request'], TRUE);

	/** validate parameters **/
	
	if(!isset($request["guess"])){
		$reply["error_message"]="Invalid request. No guess sent.";
		goto leave;
	}

	if(!is_numeric($request['guess'])){
		$reply["error_message"]="Send only numeric guesses.";
		goto leave;
	}

	/** perform operation **/
	if($request['guess']==$_SESSION['secret']){
		$reply["response"]="You got it!";
		unset($_SESSION['secret']);
		goto leave;
	}
	if($request['guess']<$_SESSION['secret']){
		$reply["response"]="Low";
		goto leave;
	}
	if($request['guess']>$_SESSION['secret']){
		$reply["response"]="High";
		goto leave;
	}

	/** leave **/
	leave: print json_encode($reply);
?>

