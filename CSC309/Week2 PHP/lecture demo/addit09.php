<?php
	session_save_path("sess");
    session_start(); // must be first thing in the php file
?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>Document Title</title>
	</head>
	<body>
		<h3>Another notation for declaring arrays</h3>
		<?php $a=array(2 => "a number", "three" => "the string three"); ?>
		<h3>And two dimenstional arrays (almost)</h3>
		<?php
			$a["stuff"]=array(1, "two", 3);

			echo("<br/>" . $a[2]);
			echo("<br/>" . $a["three"]);
			echo("<br/>" . $a["stuff"][0]);
			echo("<br/>" . $a["stuff"][1]);
		?>

		<h3>var_export</h3>
		This function takes a variable and generates PHP code which could be used
		to regenerate that variable.
		
		<p>
		The above array
<xmp>
<?php echo(var_export($a, true)); ?>
</xmp>
		</p>
		
		All things in my session
<xmp>
<?php echo(var_export($_SESSION, true)); ?>
</xmp>
		Alternatively, I can store object data as json, for example:
<xmp>
<?php echo(json_encode($_SESSION, true)); ?>
</xmp>
		Hmmm, how about I use this to store things in a file!!
	</body>
</html>
