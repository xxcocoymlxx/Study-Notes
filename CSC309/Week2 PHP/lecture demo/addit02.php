<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>addit02</title>
	</head>
	<!-- it is submitting back to the same file -->
	<!-- now php and html are combined into one file -->
	<body>
		<h3>Give me some numbers to add (all in one file)</h3>
		<form action="addit02.php">
			<input type="text" name="arg1"/>+<input type="text" name="arg2"/>
			<input type="submit"/>
		</form>
		<h3>The result</h3>
		<?php
			$answer=$_REQUEST['arg1']+$_REQUEST['arg2'];
		?>
		<?php echo $_REQUEST['arg1']?> + <?php echo $_REQUEST['arg2']?> = <?php echo $answer ?>
	</body>
</html>
