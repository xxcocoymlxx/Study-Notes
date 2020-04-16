<?php
	header('Content-Type: application/json');

	$file_name_prefix="message_data";
	$file_name=$file_name_prefix . ".txt";
	$file_lock=$file_name_prefix . ".lck";

	if(isset($_REQUEST['message'])){
		$fpLock=fopen($file_lock, 'r');
		if (flock($fpLock, LOCK_EX)) { // exclusive lock
			$messages=False;
			$s=@file_get_contents($file_name); // same as fopen, read all contents, fclose
			if($s){
				$messages=json_decode($s);
			}
			if(!$messages){
				$messages=array();
			}

			$messages[]=$_REQUEST['message'];
			
			$fp=fopen($file_name, 'w');
			fputs($fp, json_encode($messages));
			fclose($fp);

			flock($fpLock, LOCK_UN); // unlock the lock file
			fclose($fpLock);
		}
	}
	$reply=array();
	$reply['status']='ok';
	print json_encode($reply);
?>
