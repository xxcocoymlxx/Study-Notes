<html>
	<body>
		<h1>Transactions</h1>
		<?php
			$dbconn = pg_connect("host=127.0.0.1 port=5432 dbname=UTORID user=UTORID password=DB_PASSWORD");
			if(!$dbconn){
				echo("<br/>Can't connect to the database");	
				exit;
			} else {
				echo("<br/>Got a connection");
			}
		
			$insert_sells_query="INSERT INTO SELLS (SNO, PNO) VALUES ($1,$2);";
			$result = pg_prepare($dbconn, "insert_sells", $insert_sells_query);
		
		    	$insert_supplier_query="INSERT INTO SUPPLIER (SNO, CITY, SNAME) VALUES ($1, $2, $3);";
			$result = pg_prepare($dbconn, "insert_supplier", $insert_supplier_query);
		
			$result=pg_query($dbconn, "BEGIN;");
			if($result){ 
				$result = pg_execute($dbconn, "insert_supplier", array(5,"Toronto", "Canadian Tire")); 
				echo('<br/>' . pg_last_error());
				$result = pg_execute($dbconn, "insert_sells", array(5,1)); 
				echo('<br/>' . pg_last_error());
				$result = pg_execute($dbconn, "insert_sells", array(5,2)); 
				echo('<br/>' . pg_last_error());
				$result = pg_execute($dbconn, "insert_sells", array(5,3)); 
				echo('<br/>' . pg_last_error());

				/**
				PGSQL_TRANSACTION_IDLE (currently idle)
				PGSQL_TRANSACTION_ACTIVE (a command is in progress)
				PGSQL_TRANSACTION_INTRANS (idle, in a valid transaction block), 
				PGSQL_TRANSACTION_INERROR (idle, in a failed transaction block). 
				PGSQL_TRANSACTION_UNKNOWN is reported if the connection is bad. 
				PGSQL_TRANSACTION_ACTIVE is reported only when a query has been sent to the server and not yet completed. 
				**/
				$stat = pg_transaction_status($dbconn);
				if ($stat === PGSQL_TRANSACTION_INERROR) {
					echo '<br/>Error in the transaction';
					echo('<br/>' . pg_last_error());
					$result=pg_query($dbconn, "ROLLBACK;");
				} else {
					echo '<br/>Connection is in a transaction state';
					$result=pg_query($dbconn, "COMMIT;");
					if($result){ 
						echo("<br/>Committed the transaction"); 
					} else { 
						echo("<br/>could not commit the transaction"); 
						$result=pg_query($dbconn, "ROLLBACK;");
						echo('<br/>' . pg_last_error());
					}
				}    
			} else {
				echo("<br/>could not begin the transaction"); 
			}
			$result=pg_query($dbconn, "BEGIN;");
			if($result){ 
				$result = pg_execute($dbconn, "insert_sells", array(5,5)); 
				$result = pg_execute($dbconn, "insert_sells", array(5,6)); 
				$result = pg_execute($dbconn, "insert_sells", array(5,7)); 
				$result = pg_execute($dbconn, "insert_supplier", array(5,"Toronto", "Home Depot")); 

				$stat = pg_transaction_status($dbconn);
				if ($stat === PGSQL_TRANSACTION_INERROR) {
					echo '<br/>Error in the transaction';
					echo('<br/>' . pg_last_error());
					$result=pg_query($dbconn, "ROLLBACK;");
				} else {
					echo '<br/>Connection is in a transaction state';
					$result=pg_query($dbconn, "COMMIT;");
					if($result){ 
						echo("<br/>Committed the transaction"); 
					} else { 
						echo("<br/>could not commit the transaction"); 
						$result=pg_query($dbconn, "ROLLBACK;");
						echo('<br/>' . pg_last_error());
					}
				}    
			} else {
				echo("<br/>could not begin the transaction"); 
			}
		
			$result=pg_query($dbconn, "SELECT * FROM supplier;");
			while ($row = pg_fetch_array($result)) {
				echo("<br/>" . $row["sno"] . " " . $row["city"] . " " .  $row["sname"]);
			}
		?>
	</body>
</html>
		
