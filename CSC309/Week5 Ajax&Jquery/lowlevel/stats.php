<?php
	header('Content-Type: application/json');

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
	
	if(!isset($request["numbers"])){
		$reply["error_message"]="Invalid request. No numbers sent.";
		goto leave;
	}
	foreach($request["numbers"] as $number){
		if(!is_numeric($number)){
			$reply["error_message"]="Send only numbers.";
			goto leave;
		}
	}
	/** perform operation **/
	$sum = 0;
	$num = 0;
	foreach($request["numbers"] as $number){
		$sum = $sum + floatval($number);
		$num = $num + 1;
	}
	$reply["sum"]=$sum;
	$reply["num"]=$num;
	$reply["average"]=$sum/$num;

	/** leave **/
	leave: print json_encode($reply);
?>
