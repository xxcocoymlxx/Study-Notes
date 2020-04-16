<?php
	$fpLock=fopen('sharedThings.lck', 'r');
	if (flock($fpLock, LOCK_SH)) { // shared lock
		$s=file_get_contents("sharedThings.txt"); // same as fopen, read all contents, fclose
		if($s)$allSharedThings=json_decode($s, true); 
		else $allSharedThings=array();

		flock($fpLock, LOCK_UN); // unlock the lock file
		fclose($fpLock);
	}
?>
<html>
	<body>
		<h3>Sharing things</h3>
		<form> 
			Key: <input size="10" type="text" name="newKey"/>
			Value: <input size="10" type="text" name="newValue"/>
			<input type="submit" name="whichSubmit" value="add to my list" />
		</form>
		<?php 
			if(isset($_REQUEST['newKey']) && isset($_REQUEST['newValue'])){
				$allSharedThings[$_REQUEST['newKey']]=$_REQUEST['newValue']; 
				$fpLock=fopen('sharedThings.lck', 'r');
				if (flock($fpLock, LOCK_EX)) { // exclusive lock
					$fp=fopen('sharedThings.txt', 'w');
					fputs($fp, json_encode($allSharedThings));
					fclose($fp);

					flock($fpLock, LOCK_UN); // unlock the lock file
					fclose($fpLock);
				}
			}
		?>
		<h3>All Shared Things</h3>
		<ul>
		<?php
			foreach($allSharedThings as $key=>$value ){
				echo("<li> <b>$key</b> $value </li>");
			}
		?>
		</ul>
	</body>
</html>
