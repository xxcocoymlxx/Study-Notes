

--DROP TABLE IF EXISTS store;
--DROP TABLE IF EXISTS membership;
--DROP TABLE IF EXISTS beverage;
--DROP TABLE IF EXISTS orders;
--DROP TABLE IF EXISTS beverage_inventory;


DROP SCHEMA IF EXISTS fruits CASCADE;
CREATE SCHEMA fruits;

SET SEARCH_PATH to fruits;

--a Fresh Juice business with multiple stores around the country
CREATE TABLE store(
	--Each store has a city. There is only one store per city.
	city VARCHAR(50) PRIMARY KEY, 

	--Each store has a unique phone number
	phone_number  VARCHAR(10) UNIQUE NOT NULL, 

	--each store has a manager
	manager VARCHAR(50) NOT NULL
	);

--Customers can have a loyalty card if they like to go to your stores a lot.
CREATE TABLE membership(
	--a unique id number for each loyalty card holder
	id INT PRIMARY KEY, 

	--There needs to be information on how many transactions a customer made with the card
	transaction_number INT NOT NULL CHECK(transaction_number >= 0), 

	--their ‘home store’ (the one they go to most frequently).
	home_store VARCHAR(50) references store(city)
	);

--There can only be two sizes of the drinks, regular and large
CREATE TYPE drink_size AS ENUM('regular', 'large');

--All the drinks sold in the store and their detailed information
CREATE TABLE beverage(
	--Each juice beverage has a name (e.g. ‘Kiwi Lime’)
	name VARCHAR(50) NOT NULL, 
	--a drink can either be in size large or size regular
	size drink_size NOT NULL, 
	--price of each cup of drink, price can never ne lower than 0
	price REAL CHECK(price >= 0.0), 
	--calories of each cup of drink, calories can never ne lower than 0
	calories INT CHECK(calories >= 0),
	--the name and size of a drink makes a primary key of this relation
	PRIMARY KEY(name, size)
	);

--When a customer makes an order, that order should have a date, price, 
--and an indication of which loyalty card was used, if applicable.
--You can assume one beverage is ordered per transaction, 
CREATE TABLE orders(
	--unique id of each order
	id INT PRIMARY KEY, 
	--the drink that a customer ordered
	beverage_name VARCHAR(50) NOT NULL, 
	--the size of the drink that a customer ordered
	beverage_size drink_size,
	--The loyalty_card that the costomer bought the drink with, if applicable 
	loyalty_card_id INT references membership(id),
	--the date that the costomer made the order
	order_date DATE NOT NULL,

	FOREIGN KEY  (beverage_name, beverage_size) REFERENCES beverage(name, size)
	);

--Every store should keep track of the number of inventory of 
--each beverage (how much it has left in stock).
CREATE TABLE beverage_inventory(
	--a Fresh Juice store that has stocks for each kind of drink 
	city VARCHAR(10), 
	--we keep track of the beverage count by storing the latest order
	order_id INT references orders(id), 
	--the beverage count of the drink in the latest order
	beverage_count INT,
	--a store and an order_id makes a primary key of this relation
	UNIQUE(city, order_id),

	PRIMARY KEY(city, order_id)
	);

insert into store values ('Vancouver','6896678372', 'Mark'),('Toronto','6897382672', 'Larry'),('Quebec','6896671111', 'Arnold');
insert into beverage values ('kiwilime','large',7.56,900), ('kiwilime','regular',5.33,700),('apple','large',6.58,850),
	('apple','regular',4.97,650),('orange','regular',5.12,700);
insert into membership values (1234, 56, 'Vancouver'),(2468, 38, 'Toronto'),(7891, 24, 'Quebec'),
	(1396, 11, 'Toronto'),(5468, 29, 'Vancouver');
insert into orders values (01, 'apple', 'regular', 1234, '2018-05-06'), (02, 'kiwilime', 'large', 1234, '2018-05-06'),
	(03, 'orange', 'regular', 7891, '2018-08-03'),(04, 'apple', 'regular', 2468, '2018-07-07'), (05, 'orange', 'regular', 1396, '2018-06-19');
insert into beverage_inventory values ('Toronto', 04, 41), ('Quebec', 03, 62), ('Vancouver', 01, 42), 
	('Vancouver', 02, 68), ('Toronto', 05, 61);