<?php

class MasterMind {
    public $guessTimes;
    public $playerHistory;
    public $feedbacks;
    public $rightAnswer;
    public $allColors;
    public $result;

    public $starttime;
	public $endtime;
	public $time;
    
    public function __construct() {
        $this->starttime = microtime(true);
        
        $this->guessTimes = 0;

        $this->result = array("gray", "gray", "gray", "gray");

        $this->rightAnswer = array();
        $this->allColors = array("red","blue","pink","green", "brown", "orange");
        
        for ($i = 0; $i < 4; $i++){
            $num = rand(0,3);
            $this->rightAnswer[$i] = $this->allColors[$num];
        }

        $this->playerHistory = array();
        for ($i = 0; $i < 10; $i++){
            $this->playerHistory[$i] = array("gray", "gray", "gray", "gray");
        }
        
        
        $this->feedbacks = array();
        for ($i = 0; $i < 10; $i++){
            $this->feedbacks[$i] = array("gray", "gray", "gray", "gray");
        }

    }

    //receive data from controller and update the playerHistory
    public function update_history($color) {
        $guesstime = $this->guessTimes;
        $check = True;
        for ($i = 0; $i < 4; $i++){
            if($this->playerHistory[$guesstime][$i] == "gray" && $check){
                $this->playerHistory[$guesstime][$i] = $color;
                $check = False;
            }
        }
    }


    //return true if the user has 4 inputs, false otherwise
    public function check_input_valid(){
        $valid = True;
        $guesstime = $this->guessTimes;
        for ($i = 0; $i < 4; $i++){
            if($this->playerHistory[$guesstime][$i] == "gray"){
                $valid = False;
            }
        }
        return $valid;
    }



    public function delete_recent_his(){

        $guesstime = $this->guessTimes;
        for ($i = 0; $i < 4; $i++){
            $this->playerHistory[$guesstime][$i] = "gray";
        }
    }



    //check the input and update feedbacks 
    public function is_solved(){

        $black_num = 0;
        $white_num = 0;
        $index = 0;
        $solved = False;
        $input = $this->playerHistory[$this->guessTimes];

        $elementCount = array_count_values($this->rightAnswer);

        for ($i = 0; $i < 4; $i++){
            if (in_array($input[$i],$this->rightAnswer)){
                if($input[$i] == $this->rightAnswer[$i]){
                    $black_num += 1;
                    $elementCount[$input[$i]] -= 1;
                }
            }
        }
;
        for ($i = 0; $i < 4; $i++){
            if (in_array($input[$i],$this->rightAnswer) && $input[$i] != $this->rightAnswer[$i]){
               if($elementCount[$input[$i]] > 0){
                    $white_num += 1;
                    $elementCount[$input[$i]] -= 1;
               }
            }

                
        }

        if ($black_num == 4){
            $solved = True;
            $this->result = $this->rightAnswer;
        }

        while($black_num > 0) {
            $this->feedbacks[$this->guessTimes][$index] = "black";
            $black_num -= 1;
            $index += 1;
        }

        while($white_num > 0) {
            $this->feedbacks[$this->guessTimes][$index] = "white";
            $white_num -= 1;
            $index += 1;
        }

        $this->guessTimes += 1;
        if($this->guessTimes == 10){
            $this->result = $this->rightAnswer;
        }

        return $solved;
    }



}

?>