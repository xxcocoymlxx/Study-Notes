<?php

class puzzleGame {
    public $moves = 0;
    public $starttime;
	public $endtime;
	public $time;

    // 1D array of integer. 
    //Each tile will have an unique value in the [0, 15] range. 
    //Zero indicating the blank tile.
    public $tiles = array();

    //2D array representing the board
    public $board = array();

    //position of the blank tile
    public $blankpos;

    public $imgDict = array(
        0 => "images/0.png",
        1 => "images/1.png",
        2 => "images/2.png",
        3 => "images/3.png",
        4 => "images/4.png",
        5 => "images/5.png",
        6 => "images/6.png",
        7 => "images/7.png",
        8 => "images/8.png",
        9 => "images/9.png",
        10 => "images/10.png",
        11 => "images/11.png",
        12 => "images/12.png",
        13 => "images/13.png",
        14 => "images/14.png",
        15 => "images/15.png",
    );

    
    public function __construct() {
        do {
            //shuffle and generate new board
            //update tiles and board
            $this->shuffle();
            $this->starttime = microtime(true);
        } while ((!$this->isSolvable()) || ($this->isSolved()));//only half the permutation is solvable

    }


    //shuffle the values in the board 
    //leave the blank position in the solved position.
    public function shuffle(){
        $temp = array(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15);
        shuffle($temp);

        $count = 0;
        for ($i = 0; $i < 15; $i++){
            $this->tiles[$count] = $temp[$count];
            $count++;
        }

        //add the blank tile to the board
        array_push($this->tiles, 0);

        //make sure the board is up to date with tiles
        $this->board = $this->OneDToTwoD($this->tiles);
        
    }
    
    //convert a 1d array to 2d array
    public function OneDToTwoD($oneDArray){
        //initialize 2d array
        $TwoDarray = array(
            array(0,0,0,0),
            array(0,0,0,0),
            array(0,0,0,5),
            array(0,0,0,0),
        );//array to return

        $count = 0;
        for ($i = 0; $i < 4; $i++){
            for ($j = 0; $j < 4; $j++){
                    $TwoDarray[$i][$j] = $oneDArray[$count];
                    $count++;
            }
        }
        return $TwoDarray;
    }

    //convert a 2d array to 1d array
    public function TwoDToOneD($twoDArray){
        $oneDarray = array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);

        $count = 0;
        for ($i = 0; $i < 4; $i++){
            for ($j = 0; $j < 4; $j++){
                    $oneDarray[$count] = $twoDArray[$i][$j];
                    $count++;
            }
        }

        return $oneDarray;
    }


    //inversion:  Whenever a tile is preceded by a tile with higher value it counts as an inversion. 
    //with the blank tile in the solved position, 
    //the number of inversions must be even for the puzzle to be solvable.
    public function isSolvable(){
        $countInversions = 0;
        for ($i = 0; $i < 15; $i++) {
            for ($j = 0; $j < $i; $j++) {
              if ($this->tiles[$j] > $this->tiles[$i])
                $countInversions++;
            }
        }
        return $countInversions % 2 == 0;
    }


    //we iterate on the tiles in reverse order and 
    //if a tile value is different from the corresponding index + 1, 
    //we return false. 
    public function isSolved(){
        // if blank tile is not in the solved position ==> not solved
        if ($this->tiles[15] != 0){ 
            return false;
        }

        for ($i = 14; $i >= 0; $i--) {
            if (isset($this->tiles[$i])){
                if (($this->tiles[$i]) != ($i + 1)){
                    return false;	
                }
            }else {
                return false;		
        }

       return true;
    }
}

//return true if current clicked index can move
//(one of it's surrouding clock is blank)
//already moved if movable
public function checkIfMoveable($rowCoordinate, $columnCoordinate, $direction){
    $this->moves++;
    $rowOffset = 0;
    $columnOffset = 0;

    if ($direction == "up")
  {
    $rowOffset = -1;
  }
  else if ($direction == "down")
  {
    $rowOffset = 1;
  }
  else if ($direction == "left")
  {
    $columnOffset = -1;
  }
  else if ($direction == "right")
  {
    $columnOffset = 1;
  }  
    // Check if the tile can be moved to the spot.
  // If it can, move it and return true.
  if ($rowCoordinate + $rowOffset >= 0 && $columnCoordinate + $columnOffset >= 0 
  && $rowCoordinate + $rowOffset < 4 && $columnCoordinate + $columnOffset < 4){
  if ($this->board[$rowCoordinate + $rowOffset][$columnCoordinate + $columnOffset] == 0){
    $this->board[$rowCoordinate + $rowOffset][$columnCoordinate + $columnOffset] = $this->board[$rowCoordinate][$columnCoordinate];
    $this->board[$rowCoordinate][$columnCoordinate] = 0;
    $this->tiles = $this->TwoDToOneD($this->board);//update the 1d board as well   
    return true;
  }
}
return false; 
}

//return true if movable and moved, otherwise return false
public function moveThisTile($tableRow, $tableColumn){
    if ($this->checkIfMoveable($tableRow, $tableColumn, "up") ||
    $this->checkIfMoveable($tableRow, $tableColumn, "down") ||
    $this->checkIfMoveable($tableRow, $tableColumn, "left") ||
    $this->checkIfMoveable($tableRow, $tableColumn, "right") )
  {
      //the board and tiles are both updated now
      return true;
  }else{
    return false;
  }
}

//arg: new arrangement of the images
public function getNewBoard(){
    return array(
        0=> $this->imgDict[$this->tiles[0]],
        1=> $this->imgDict[$this->tiles[1]],
        2=> $this->imgDict[$this->tiles[2]],
        3=> $this->imgDict[$this->tiles[3]],
        4=> $this->imgDict[$this->tiles[4]],
        5=> $this->imgDict[$this->tiles[5]],
        6=> $this->imgDict[$this->tiles[6]],
        7=> $this->imgDict[$this->tiles[7]],
        8=> $this->imgDict[$this->tiles[8]],
        9=> $this->imgDict[$this->tiles[9]],
        10=> $this->imgDict[$this->tiles[10]],
        11=> $this->imgDict[$this->tiles[11]],
        12=> $this->imgDict[$this->tiles[12]],
        13=> $this->imgDict[$this->tiles[13]],
        14=> $this->imgDict[$this->tiles[14]],
        15=> $this->imgDict[$this->tiles[15]],
    );
}
}
?>