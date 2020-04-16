<h1>PHP-Postgresql</h1>
<ul>
<li><a href=http://php.net/manual/en/book.pgsql.php>PHP-PostgreSQL</a>
<li> To setup this example, first grab <a href=schema.sql>schema.sql</a>
<li> login to cslinux, 
<xmp>
psql
\i schema.sql
</xmp>
<li> Your database name is UTORID, your database user name is your UTORID, 
your database password is the last 5 digits of your t-card barcode before the last two digits.
So in python libraryBarcode[-7:-2]. You will need to put these into the examples.php and transactions.php scripts.
</ul>
<?php
	
	$dbconn = pg_connect("host=127.0.0.1 port=5432 dbname=UTORID user=UTORID password=DB_PASSWORD");
	if(!$dbconn){
		echo("Can't connect to the database");	
		exit;
	}
	# send an unparameterized query
	$result=pg_query($dbconn, "INSERT INTO PART (PNO, PNAME, PRICE ) VALUES (10,'Screw',10);");
	if($result){
		$rows_affected=pg_affected_rows($result);
       		echo("rows_affected=$rows_affected");
	} else {
		echo("Could not execute query");
	}

	# A PreparedStatement is a parameterized SQL statement
	$insert_sells_query="INSERT INTO SELLS (SNO, PNO) VALUES ($1,$2);";
	$result = pg_prepare($dbconn, "my_query", $insert_sells_query);
	$result = pg_execute($dbconn, "my_query", array(1,10)); # fill in the $1 and $2 respectively and run query
	if($result){
		$rows_affected=pg_affected_rows($result);
       		echo("rows_affected=$rows_affected");
	} else {
		echo("Could not execute query");
	}

	# can continue to do this...
	# $result = pg_execute($dbconn, "my_query", array(2,20)); # fill in the $1 and $2 respectively and run query
	# $rows_affected=pg_affected_rows($result);
	# $result = pg_execute($dbconn, "my_query", array(3,50)); # fill in the $1 and $2 respectively and run query
	# $rows_affected=pg_affected_rows($result);
	# ...

	# $query="SELECT * FROM PART;"; # better to be explicit!
	$query="SELECT PNO, PNAME, PRICE FROM PART;";
	echo("<br/>about to execute $query");

	# Send the query to the DB.
	# A ResultSet is returned when we execute a search query.
 	# This allows us to scroll through the rows of the result
 	# table one row at a time

	$result=pg_query($dbconn, $query);

	// Go through all rows returned by the query
	while ($row = pg_fetch_row($result)) {
		// Pull out individual columns from the current row
		#           PNO     PNAME    PRICE
		echo("<br/>$row[0], $row[1], $row[2]");
	}

	$result=pg_query($dbconn, $query);

	// Go through all rows returned by the query
	while ($row = pg_fetch_array($result)) {
		// Pull out individual columns from the current row
		#           PNO     PNAME    PRICE
		echo("<br/>$row[pno], $row[pname], $row[price]");
	}
	# From the manual: Using pg_close() is not usually necessary, as 
	# non-persistent open connections are automatically closed at the end of the script. 
?>

