<?php
	// functions that help with view generation

	// return the errors in a standard format
	function view_errors($errors){
		$s="";
		foreach($errors as $key=>$value){
			$s .= "<br/> $value";
		}
		return $s;
	}

?>
