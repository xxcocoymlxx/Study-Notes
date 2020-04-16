<?php
	session_save_path("sess");
    session_start(); // must be first thing in the php file
	if(!isset($_SESSION['mappedThings']))$_SESSION['mappedThings']=array();
	$allMappedThings=&$_SESSION['mappedThings']; 
?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>addit08</title>
	</head>
	<body>
		<h3>A note on assignments (=)</h3>
		In php, a=b means copy the value of b to a. The value is NOT the address (unlike Java)
		<h3>Arrays as maps</h3>
		They can have string or integer indices.
		<?php
			$a=array();
			$a[23]="twenty three";
			$a["orange"]="juice";
			$a["forty five"]=45;
			$a[1.345]=27;
			$a[1.57]=28; // floating point indices get truncated!
			$a[false]="False"; // booleans get converted to integers (false=0, true=1)
			echo("<ul>");
			foreach($a as $key=>$value ){
				echo("<li> <b>$key</b> $value </li>");
			}
			echo("</ul>");
		?>
		<h3>Example</h3>
		<form> 
			Key: <input size="10" type="text" name="newKey"/>
			Value: <input size="10" type="text" name="newValue"/>
			<input type="submit" name="whichSubmit" value="add to my list" />
		</form>
		<?php 
			if(isset($_REQUEST['newKey']) && isset($_REQUEST['newValue'])){
				$allMappedThings[$_REQUEST['newKey']]=$_REQUEST['newValue']; 
			}
				
		?>
		<h3>Mapped Things in my session</h3>
		<ul>
		<?php
			foreach($allMappedThings as $key=>$value ){
				echo("<li> <b>$key</b> $value </li>");
			}
		?>
		</ul>
		<h3>Things in my session (from last page)</h3>
		<ul>
		<?php
			foreach($_SESSION['things'] as $key=>$value ){
				echo("<li> <b>$key</b> $value </li>");
			}
		?>
		</ul>
		<h3>Actions</h3>
		<a href="destroySession.php">Destroy Session</a>

		<h3>Exercises</h3>
		<ul>
		</ul>
	</body>
</html>
