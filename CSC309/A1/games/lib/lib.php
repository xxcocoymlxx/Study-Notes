<?php
	require_once "dbconnect_string.php";
        function db_connect(){
                global $g_dbconnect_string;
                $dbconn = pg_connect($g_dbconnect_string);
                if(!$dbconn){
			$system_errors[] = "Can't connect to the database.";
			return null;
		} else return $dbconn;
        }

	// return the errors in a standard format
        function view_errors($e){
                $s="";
                foreach($e as $key=>$value){
                        $s .= "<br/> $value";
                }
                return $s;
        }
?>
