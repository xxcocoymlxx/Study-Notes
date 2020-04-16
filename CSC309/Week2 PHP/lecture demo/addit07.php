<?php
	session_save_path("sess");
    session_start(); // must be first thing in the php file
	// setup session variables
	// arrays can store anything
	if(!isset($_SESSION['things']))$_SESSION['things']=array(1,"a string", 3.143, true);

	// $allThings=$_SESSION['things']; // would copy the array

	// $allThings is a reference to the array so I don't have to write $_SESSION['things'][]
	$allThings=&$_SESSION['things']; 
?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>addit07</title>
	</head>
	<body>
		<h3>Arrays</h3>
		<form> 
			<input size="2" type="text" name="newThing"/>
			<input type="submit" name="whichSubmit" value="add to my list" />
		</form>
		<?php 
			if(isset($_REQUEST['newThing'])){
				$allThings[]=$_REQUEST['newThing']; // add to the end of the array
			}
				
		?>
		<h3>Things in my session (foreach loop)</h3>
		<ul>
		<?php
			foreach($allThings as $key=>$value ){
				echo("<li> <b>$key</b> $value </li>");
			}
		?>
		<h3>Arrays are more general than that!!!</h3>
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
		</ul>
		<h3>Exercises</h3>
		<ul>
		</ul>
	</body>
</html>
