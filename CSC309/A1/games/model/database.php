<?php

class Database {
    public $dbconn = null;

    public function __construct() {
        $this->dbconn = db_connect();
    }

    public function getUserInfo($username){
        //get all the information of the user from the database
		$query = "SELECT * FROM appuser WHERE userid=$1;";
        $result = pg_prepare($this->dbconn, "", $query);
		$result = pg_execute($this->dbconn, "", array($username));

		//returns an array that corresponds to the fetched row (record).
		//PGSQL_ASSOC: result is indexed associatively (indexed by field name),
        $row = pg_fetch_array($result, NULL, PGSQL_ASSOC);
        return $row;
    }

    //return true if user is registered (has username and password in database)
    public function registeredUser($username,$password){
        $query = "SELECT * FROM appuser WHERE userid=$1 and password=$2;";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", array($username, $password));
        if($row = pg_fetch_array($result, NULL, PGSQL_ASSOC)){
            return TRUE;
        }else {
            return FALSE;
        }
    }

    public function usernameExists($username){
        //check if username is already in database
		$query = "SELECT * FROM appuser WHERE userid=$1;";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", array($username));
        if ($row = pg_fetch_array($result, NULL, PGSQL_ASSOC)){
            return True;
        }else {
            return False;
        }
    }

    //return false if insertion fails
    public function createNewUser($params){
        //params is array of values to be put into database
        $query = "INSERT INTO appuser (userid, password, gender, birthday, gift,subscribe) values($1, $2,$3,$4,$5,$6);";
		$result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params);
        
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    //return false if update fails
    public function updatePassword($params){
        $query = "UPDATE appuser appuser SET password = $1 WHERE userid = $2;";
		$result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    //return false if update fails
    public function updateGender($params){
            $query = "UPDATE appuser appuser SET gender = $1 WHERE userid = $2;";
            $result = pg_prepare($this->dbconn, "", $query);
            $result = pg_execute($this->dbconn, "", $params); 
            //A query result resource on success or FALSE on failure.
            return $result;
        }
    //return false if update fails
    public function updateBirthday($params){
        $query = "UPDATE appuser appuser SET birthday = $1 WHERE userid = $2;";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    //return false if update fails
    public function updateSub($params){
        $query = "UPDATE appuser appuser SET subscribe = $1 WHERE userid = $2;";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    public function GuessGameStats($params){
        $query = "INSERT INTO GuessGame VALUES($1, $2, $3,$4);";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    public function MasterMindStats($params){
        $query = "INSERT INTO MasterMind VALUES($1, $2, $3,$4);";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    public function PegSolitareStats($params){
        $query = "INSERT INTO PegSolitare VALUES($1, $2, $3,$4);";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    public function PuzzleGameStats($params){
        $query = "INSERT INTO PuzzleGame VALUES($1, $2, $3,$4);";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    //------------------------------for Game Stats---------------------------------
    public function GetMasterMindStats(){
        $query = "select userid, min(moves+sec) as bestresult from MasterMind GROUP BY userid ORDER BY bestresult;";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", array()); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    public function GetPegSolitareStats(){
        $query = "select userid, min(moves+sec) as bestresult from PegSolitare GROUP BY userid ORDER BY bestresult;";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", array()); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    public function GetPuzzleGameStats(){
        $query = "select userid, min(moves+sec) as bestresult from PuzzleGame GROUP BY userid ORDER BY bestresult;";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", array()); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    public function GetGuessGameStats(){
        $query = "select userid, min(moves+sec) as bestresult from GuessGame GROUP BY userid ORDER BY bestresult;";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", array()); 
        //A query result resource on success or FALSE on failure.
        return $result;
    }

    public function GetGuessGamePersonalBest($params){
        $query = "SELECT moves, sec FROM GuessGame WHERE userid = $1 ORDER BY (sec+moves);";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        //A query result resource on success or FALSE on failure.
        $row = pg_fetch_all($result, PGSQL_ASSOC);
        return $row;
    }

    public function GetPuzzleGamePersonalBest($params){
        $query = "SELECT moves, sec FROM PuzzleGame WHERE userid = $1 ORDER BY (sec+moves);";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        $row = pg_fetch_all($result,PGSQL_ASSOC);
        //A query result resource on success or FALSE on failure.
        return $row;
    }

    public function GetMasterMindPersonalBest($params){
        $query = "SELECT moves, sec FROM MasterMind WHERE userid = $1 ORDER BY (sec+moves);";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        $row = pg_fetch_all($result,PGSQL_ASSOC);
        //A query result resource on success or FALSE on failure.
        return $row;
    }

    public function GetPegSolitarePersonalBest($params){
        $query = "SELECT moves, sec FROM PegSolitare WHERE userid = $1 ORDER BY (sec+moves);";
        $result = pg_prepare($this->dbconn, "", $query);
        $result = pg_execute($this->dbconn, "", $params); 
        $row = pg_fetch_all($result, PGSQL_ASSOC);
        //A query result resource on success or FALSE on failure.
        return $row;
    }


}



?>