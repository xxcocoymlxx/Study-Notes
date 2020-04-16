<html>
	<body>
		<h3>Datatypes</h3>
		<ul>
		<li> Booleans
			<?php
			$v=True; $v=False; $v=True && (False || True);
			echo($v);
			?>
			The following are considered false...
			<xmp>FALSE, 0, 0.0, "", '', "0", Array()</xmp>
			Other values are considered True.
		<li> Integers
			<?php
			$v=1; $v=-1; $v=3; $v=$v*2;
			echo($v);
			?>
		<li> Floating point numbers
			<?php
			$v=3.14159; $v=$v*1.2e3;
			echo($v);
			?>
		<li> Strings
			<?php
			$w="I am Sid";
			$v='Hello There $w'; # no interpolation
			echo("<br/>$v"); 
			$v="Hello There $w"; #variable interpolation
			echo("<br/>$v"); 
			$v=<<<EOS1
This is a 'heredoc'
it spans many lines.
It can include all kinds of 	things. Including
$w $w interpolated variables.
EOS1;
			echo("<br/>$v");
			$v= "This is " . " string concatenation ";
			$v=$v . $v;
			echo("<br/>$v");
			# strings are considered arrays of their characters
			echo("<br/>" . $v[0]);
			echo("<br/>" . $v[1]);
			echo("<br/>" . $v[2]);
			?>
		<li> Arrays: Ordered maps
			<?php
			$v=array('a','b','c','d');
			echo("<br/>$v[0]");
			echo("<br/>$v[1]");
			echo("<br/>$v[2]");
			echo("<br/>$v[3]");
			echo("<br/>x$v[4]x"); # hmmm, whats happening here?
			$v=array(1,2.34,'c',array(0,1,True));
			echo("<br/>$v[0]");
			echo("<br/>$v[1]");
			echo("<br/>$v[2]");
			echo("<br/>$v[3]");
			echo("<br/>$v[3][0]"); # oops, interpolation error
			echo("<br/>" . $v[3][0]); # string concat
			echo("<br/>" . $v[3][1]);
			echo("<br/>" . $v[3][2]); # hmm, True turned in to an integer
			?>
			<br/>Now some really neat things about arrays...
			<br/>Arrays in PHP are associative...they are indexed by keys and have values...
			<p>A key may be either an integer or a string. 
			If a key is the standard representation of an integer, 
			it will be interpreted as such (i.e. "8" will be interpreted as 8, 
			while "08" will be interpreted as "08"). 
			Floats in key are truncated to integer. 
			The indexed and associative array types are the same type in PHP, which can both contain integer and string indices. 
			</p>
			<?php
			$v=array('a','b','c','d');
			$v[]="this is a new element"; # appending to the end of an array
			echo("<br/>$v[4]");
			$v[]="and another new element";
			echo("<br/>$v[5]");
			$v=array("apple"=>"good", "peach"=>"bad", "nouns"=>array("car", "boat", "cell phone"), 2=>"snake eyes");
			echo("<br/>$v[0]"); #hmmm, there is no element 0
			echo("<br/>$v[2]");
			echo("<br/>$v[apple]");
			echo("<br/>$v[peach]");
			echo("<br/>$v[bad]"); # explain this
			echo("<br/>" . $v[nouns][0]); 
			echo("<br/>" . $v[nouns][1]); 
			echo("<br/>" . $v[nouns][2]); 
			$v[]="a new element, where does it live?";
			echo("<br/>$v[0]"); # not here
			echo("<br/>$v[3]"); # oh there it is!!
			# If a key is not specified for a value, the maximum of the integer indices is taken and the new key will be that value plus 1.
			?>
		<li> We did not cover...Objects, Resources, NULL
		</ul>
		<h3>Type Juggling</h3>
		<p>
		PHP does not require (or support) explicit type definition in variable declaration; a variable's type is determined by the context in which the variable is used. That is to say, if a string value is assigned to variable $var, $var becomes a string. If an integer value is then assigned to $var, it becomes an integer. 
		</p>
		From <a href=manual/html/language.types.type-juggling.html>the manual</a>
		
	</body>
</html>
