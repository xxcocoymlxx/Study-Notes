<?php

class GuessGame {
	public $secretNumber = 5;
	public $numGuesses = 0;
	public $history = array();
	public $state = "";
	public $starttime;
	public $endtime;
	public $time;


	public function __construct() {
			$this->secretNumber = rand(1,10);
			$this->starttime = microtime(true);
    	}
	
	public function makeGuess($guess){
		$this->numGuesses++;
		if($guess>$this->secretNumber){
			$this->state="too high";
		} else if($guess<$this->secretNumber){
			$this->state="too low";
		} else {
			$this->state="correct";
		}
		$this->history[$this->numGuesses-1] = "Guess #$this->numGuesses was $guess and was $this->state.";

	}

	public function getState(){
		return $this->state;
	}
}
?>
