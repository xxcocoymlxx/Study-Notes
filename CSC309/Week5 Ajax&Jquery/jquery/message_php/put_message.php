<?php
	$file_name_prefix="message_data";
	$file_name=$file_name_prefix . ".txt";
	$file_lock=$file_name_prefix . ".lck";

	$fpLock=fopen($file_lock, 'w');
	if (flock($fpLock, LOCK_SH)) { // shared lock
		$messages=False;
		$s=@file_get_contents($file_name); // same as fopen, read all contents, fclose
		if($s){
			$messages=unserialize($s);
		}
		if(!$messages){
			$messages=array();
		}

		flock($fpLock, LOCK_UN); // unlock the lock file
		fclose($fpLock);
	}
	if(isset($_REQUEST['message'])){
		$messages[]=$_REQUEST['message']; 
		$fpLock=fopen($file_lock, 'r');
		if (flock($fpLock, LOCK_EX)) { // exclusive lock
			$fp=fopen($file_name, 'w');
			fputs($fp, serialize($messages));
			fclose($fp);

			flock($fpLock, LOCK_UN); // unlock the lock file
			fclose($fpLock);
		}
	}
?>
OK!
