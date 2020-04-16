<html>
	<body>
		<h3>Give me some numbers to add (all in one file)</h3>
		<form action="echoit.php">
			<input type="text" name="arg1"/>+<input type="text" name="arg2"/>
			<input type="submit"/>
		</form>
		<h3>The result</h3>
		<?php
			$answer=$_REQUEST['arg1']+$_REQUEST['arg2'];
		?>
		<?php echo $_REQUEST['arg1']?> + <?php echo $_REQUEST['arg2']?> = <?php echo $answer ?>
		<br/>
		<?php echo("$_REQUEST[arg1]+$_REQUEST[arg2]=$answer"); ?>
		<?= $answer ?>
	</body>
</html>
