<?php
	header('Content-Type: application/json');
	$file_name_prefix="message_data";
	$file_name=$file_name_prefix . ".txt";
	$file_lock=$file_name_prefix . ".lck";

	$fpLock=fopen($file_lock, 'w');
	if (flock($fpLock, LOCK_SH)) { // shared lock
		$messages=False;
		$s=@file_get_contents($file_name); // same as fopen, read all contents, fclose
		if($s){
			$messages=json_decode($s);
		}
		if(!$messages){
			$messages=array();
		}

		flock($fpLock, LOCK_UN); // unlock the lock file
		fclose($fpLock);
	}
	$reply=array();
	$reply['status']='ok';
	$reply['messages']=$messages;
	print json_encode($reply);
?>
