-- Dropping and creating a table (note PRIMARY KEY)
DROP TABLE part;
CREATE TABLE part (
	pno integer PRIMARY KEY,
	pname VARCHAR(20),
	price real
);

-- Adding rows to a table
INSERT INTO part (pno,pname,price) VALUES(1,'Screw',10);
INSERT INTO part (pno,pname,price) VALUES(2,'Nut',8);
INSERT INTO part (pno,pname,price) VALUES(3,'Bolt',15);
INSERT INTO part (pno,pname,price) VALUES(4,'Cam',25);

-- oops, following violates primary key
INSERT INTO part (pno,pname,price) VALUES(4,'Hammer',25);


-- Note NOT NULL
DROP TABLE supplier;
CREATE TABLE supplier (
	sno integer PRIMARY KEY,
	sname VARCHAR(20) NOT NULL,
	city VARCHAR(20)
);
INSERT INTO supplier VALUES(1,'Smith','London');
INSERT INTO supplier VALUES(2,'Jones','Paris');
INSERT INTO supplier VALUES(3,'Adams','Vienna');
INSERT INTO supplier VALUES(4,'Blake','Rome');

DROP TABLE sells;
CREATE TABLE sells (
	sno integer,
	pno integer,
	PRIMARY KEY(sno,pno)
);
INSERT INTO sells VALUES(1,1);
INSERT INTO sells VALUES(1,2);
INSERT INTO sells VALUES(2,4);
INSERT INTO sells VALUES(3,1);
INSERT INTO sells VALUES(3,3);
INSERT INTO sells VALUES(4,2);
INSERT INTO sells VALUES(4,3);
INSERT INTO sells VALUES(4,4);

-- Selects (* means all fields)
-- SELECT fields
-- FROM relations
-- WHERE condition

SELECT * 
FROM PART; 

SELECT * 
FROM PART 
WHERE PRICE > 10; 

SELECT PNAME, PRICE 
FROM PART 
WHERE PRICE > 10; 

SELECT PNAME, PRICE 
FROM PART 
WHERE PNAME = 'Bolt' AND (PRICE = 0 OR PRICE <= 15);

-- Cartesian products
SELECT * 
FROM SUPPLIER, PART;

-- Cartesian product of supplier with itself, S1 and S2 are 
-- names for each copy of the table
SELECT * 
FROM SUPPLIER S1, SUPPLIER S2;

-- All suppliers and the parts they sell
SELECT S.SNAME, P.PNAME
FROM SUPPLIER S, PART P, SELLS SE
WHERE S.SNO = SE.SNO AND P.PNO = SE.PNO;

-- Modify the above query to list all suppliers of Bolts.

-- Order By
SELECT S.SNAME, P.PNAME
FROM SUPPLIER S, PART P, SELLS SE
WHERE S.SNO = SE.SNO AND P.PNO = SE.PNO
ORDER BY S.SNAME;

-- Data Manipulation
INSERT INTO SUPPLIER (SNO, SNAME, CITY) VALUES (1, 'Smith', 'London');
UPDATE PART SET PRICE = 15 WHERE PNAME = 'Screw';
DELETE FROM SUPPLIER WHERE SNAME = 'Smith';

-- Creating indexes
CREATE UNIQUE INDEX supplierIndex ON supplier (SNO );
