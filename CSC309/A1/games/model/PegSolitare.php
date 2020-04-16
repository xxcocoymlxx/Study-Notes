<?php

class chessPiece {

    public $color;
    public $chessNumber;
    public $possibleSpot;
    public $starttime;
	public $endtime;
    public $time;
    public $moves;

    public function __construct($color, $chessNumber) {
        $this->starttime = microtime(true);
        $this->color = $color;
        $this->chessNumber = $chessNumber;
        if($chessNumber == 0){
            $this->possibleSpot = array(6,8);
        }else if($chessNumber == 2){
            $this->possibleSpot = array(4,10);
        }else if($chessNumber == 3){
            $this->possibleSpot = array(5,9,11);
        }else if($chessNumber == 4){
            $this->possibleSpot = array(2,10,12);
        }else if($chessNumber == 5){
            $this->possibleSpot = array(3,11);
        }else if($chessNumber == 6){
            $this->possibleSpot = array(0,8,14);
        }else if($chessNumber == 7){
            $this->possibleSpot = array();
        }else if($chessNumber == 8){
            $this->possibleSpot = array(0,6,14);
        }else if($chessNumber == 9){
            $this->possibleSpot = array(3,11);
        }else if($chessNumber == 10){
            $this->possibleSpot = array(2,4,12);
        }else if($chessNumber == 11){
            $this->possibleSpot = array(3,5,9);
        }else if($chessNumber == 12){
            $this->possibleSpot = array(4,10);
        }else if($chessNumber == 14){
            $this->possibleSpot = array(6,8);
        }else{
            echo "invalid number";
        }
    }


}

class pegSolitareBoard {
    public $picked;
    public $dropSpot;
    public $allPieces = array(1,2,3,4,5,6,7,8);

    public $chessPicked;
    public $firstPick;
    public $moves;

    public $starttime;
	public $endtime;
	public $time;

    public function __construct() {
        $this->starttime = microtime(true);
        $this->moves = 0;
        $this->allPieces[0] = new chessPiece("red", 0);
        $this->allPieces[1] = new chessPiece("red", 2);
        $this->allPieces[2] = new chessPiece("red", 3);
        $this->allPieces[3] = new chessPiece("red", 4);
        $this->allPieces[4] = new chessPiece("red", 5);
        $this->allPieces[5] = new chessPiece("red", 6);
        $this->allPieces[6] = new chessPiece("red", 7);
        $this->allPieces[7] = new chessPiece("red", 8);
        $this->allPieces[8] = new chessPiece("red", 9);
        $this->allPieces[9] = new chessPiece("red", 10);
        $this->allPieces[10] = new chessPiece("red", 11);
        $this->allPieces[11] = new chessPiece("red", 12);
        $this->allPieces[12] = new chessPiece("red", 14);

        $number = rand(0,12);
        while ($number == 6){
            $number = rand(0,12);
        }
        $this->allPieces[$number]->color = "white";

        $this->chessPicked = False;
        $this->firstPick = True;

    }

    public function movePieces() {
        
        if(in_array($this->dropSpot->chessNumber, $this->picked->possibleSpot)){
            $this->picked->color = "white";
            $this->dropSpot->color = "red";
            
            $num = ($this->picked->chessNumber + $this->dropSpot->chessNumber) / 2;
            $this->allPieces[$num-1]->color = "white";

            $this->chessPicked = False;
            $this->moves++;
            if($this->is_solved()){
                echo "you win!!!!!!!!!!!!!";
            }
        }

    }


    public function is_solved(){
        $check = 0;
        for ($i = 0; $i < 13; $i++) {
            if($this->allPieces[$i]->color == "red"){
                $check += 1;
            }
        }
        if ($check == 1){
            return True;
        }else{
            return False;
        }
    }




    public function process_action($num){
        if($this->firstPick && $this->allPieces[$num]->color == "red"){
            $this->picked = $this->allPieces[$num];
            $this->chessPicked = True;
            $this->firstPick = False;
        }else if($this->chessPicked){        //we are dropping
            if($this->allPieces[$num]->color == "white"){
                $this->dropSpot = $this->allPieces[$num];
                $this->movePieces();
            }else{
                $this->chessPicked = False;
            }
        }else if(!$this->chessPicked){     //we are picking
            if($this->allPieces[$num]->color == "red"){
                $this->picked = $this->allPieces[$num];
                $this->chessPicked = True;
            }else{
                $this->chessPicked = False;
            }
            
        }
    }





}


?>
