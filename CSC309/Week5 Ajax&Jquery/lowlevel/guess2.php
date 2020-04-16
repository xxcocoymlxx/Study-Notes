<?php
	session_save_path("sess");
	session_start();
	if(!isset($_SESSION['secret'])){
		$_SESSION['secret']=rand(1,10);
	}
	if(isset($_REQUEST['guess'])){
		if($_REQUEST['guess']<$_SESSION['secret']){
			$reply="small";
		} else if($_REQUEST['guess']>$_SESSION['secret']){
			$reply="large";
		} else {
			$reply="correct";
			unset($_SESSION['secret']);
		}
	}
	echo($reply);
?>
