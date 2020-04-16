DROP TABLE supplier CASCADE;
DROP TABLE sells CASCADE;
DROP TABLE part CASCADE;

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
CREATE TABLE supplier (
	sno integer PRIMARY KEY,
	sname VARCHAR(20) NOT NULL,
	city VARCHAR(20)
);
INSERT INTO supplier VALUES(1,'Smith','London');
INSERT INTO supplier VALUES(2,'Jones','Paris');
INSERT INTO supplier VALUES(3,'Adams','Vienna');
INSERT INTO supplier VALUES(4,'Blake','Rome');

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

