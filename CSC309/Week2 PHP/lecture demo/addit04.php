<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>addit04</title>
	</head>
	<body>
		<h3>Give me some numbers</h3>
		<form> <!-- if I am submitting back here, I don't need the action -->
			<input size="2" type="text" name="arg1"/>
			<select name="operation">
				<option>+</option>
				<option>-</option>
				<option>*</option>
				<option>/</option>
			</select>
			<input size="2" type="text" name="arg2" />
			<input type="submit" name="whichSubmit" value="=" />
		</form>
		<?php if(isset($_REQUEST['whichSubmit'])){ ?>
			<h3>The result</h3>
			<?php
				if($_REQUEST['operation']=='+')$answer=$_REQUEST['arg1']+$_REQUEST['arg2'];
				if($_REQUEST['operation']=='-')$answer=$_REQUEST['arg1']-$_REQUEST['arg2'];
				if($_REQUEST['operation']=='*')$answer=$_REQUEST['arg1']*$_REQUEST['arg2'];
				if($_REQUEST['operation']=='/')$answer=$_REQUEST['arg1']/$_REQUEST['arg2'];
			?>
			<?php echo $_REQUEST['arg1']?> <?php echo $_REQUEST['operation']?> <?php echo $_REQUEST['arg2']?> = <?php echo $answer ?>
		<?php } ?>
	</body>
</html>
