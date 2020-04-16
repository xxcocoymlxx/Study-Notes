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
