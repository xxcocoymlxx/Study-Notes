--- load with 
--- sqlite3 database.db < schema.sql

CREATE TABLE counter (
	counterName VARCHAR(20) PRIMARY KEY,
	counterValue INTEGER DEFAULT 0
);
