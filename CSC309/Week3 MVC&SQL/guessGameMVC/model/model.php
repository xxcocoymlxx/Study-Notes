<?php
	/* model */
	function make_guess($guess){
		$_SESSION["numGuesses"]++;
		if($guess>$_SESSION["secretNumber"]){
			$result="too high";
		} else if($guess<$_SESSION["secretNumber"]){
			$result="too low";
		} else {
			$result="correct";
		}
		$_SESSION["history"][] = "Guess #$_SESSION[numGuesses] was $guess and was $result.";
		return($result);
	}

	function start_game(){
		$_SESSION["secretNumber"]=rand(1,10);
		$_SESSION["numGuesses"]=0;
		$_SESSION["history"]=array();
	}
?>
