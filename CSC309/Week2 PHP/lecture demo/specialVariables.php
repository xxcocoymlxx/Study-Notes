<html>
	<body>
<xmp>
<?php
foreach ($_SERVER as $key=>$value){
	echo("\$_SERVER[$key]=$value\n");
}
?>
</xmp>

<?php
writeArray($_SERVER, "\$_SERVER");
writeArray($_REQUEST, "\$_REQUEST");
?>
	</body>
</html>
<?php
function writeArray($a, $name){
	echo "<xmp>";
	foreach ($a as $key=>$value){
		echo("$name" . "[$key]=$value\n");
	}
	echo "</xmp>";
}
?>
