<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>addit03</title>
	</head>
	<body>
		<h3>Give me some numbers to add (all in one file)</h3>
		<form> <!-- if I am submitting back here, I don't need the action -->
			<input size="2" type="text" name="arg1"/>+<input size="2" type="text" name="arg2"/>
			<input type="submit" name="whichSubmit" value="Give me the answer">
			<input type="submit" name="whichSubmit" value="Dont Give me the answer">
			<br/><b>Exercise:</b>Fix the second button
		</form>
		<?php if(isset($_REQUEST['whichSubmit']) && $_REQUEST['whichSubmit']=="Give me the answer"){ ?>
			<h3>The result</h3>
			<?php
				$answer=$_REQUEST['arg1']+$_REQUEST['arg2'];
			?>
			<?php echo $_REQUEST['arg1']?> + <?php echo $_REQUEST['arg2']?> = <?php echo $answer ?>
		<?php } ?>
	</body>
</html>
