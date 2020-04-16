<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>addit06</title>
	</head>
	<body>
		<h3>For Loops</h3>
		<form> 
			<input size="2" type="text" name="num"/>
			<input type="submit" name="whichSubmit" value="sum up" />
		</form>
		<?php 
			if(isset($_REQUEST['num'])){
				$n=$_REQUEST['num'];
				for($i=0;$i<=$n;$i++){
					$total=$total+$i;
				}
				echo("0+...+$n=$total<br/>"); // String interpolation inside "
				echo('0+...+$n=$total<br/>'); // String interpolation not inside '
			}
				
		?>
		<h3>While loops</h3>
		<?php
			$fib1=1; $fib2=1; $j=0;
			echo("$fib1");
			while($j<10){
				echo(",$fib2");
				$temp=$fib1+$fib2;
				$fib1=$fib2;
				$fib2=$temp;
				$j++;
			}
		?>
		<h3>Exercises</h3>
		<ul>
		<li> Modify this so that it actually prints out all the numbers from 0 to n
			for example 0+1+2+3+4=10
		</li> 
		<li> Modify this so that it prints out the first n Fibonacci numbers
			Hint: add another form with a different value (or name) for the submit button.
			Use this to determine which operation to perform.
		</li> 
		<li> As an alternative to 'echo' above, build up the output strings and then just echo the final
			string. Note: String concatenation looks like...
<xmp>
	$a="this is";
	$b=$a . " a test!";
	$c=$a . "ZZ" . $b . $a;
</xmp>
		</li> 
		</ul>
	</body>
</html>
