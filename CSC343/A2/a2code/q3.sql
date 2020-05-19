-- Committed

SET SEARCH_PATH TO parlgov;
drop table if exists q3 cascade;

-- You must not change this table definition.

CREATE TABLE q3(
        countryName VARCHAR(50),
        partyName VARCHAR(100),
        partyFamily VARCHAR(50),
        stateMarket REAL
);


DROP VIEW IF EXISTS recentCabParty CASCADE;
DROP VIEW IF EXISTS ShouldHaveBeen CASCADE;
DROP VIEW IF EXISTS notcommittedParty CASCADE;
DROP VIEW IF EXISTS COMBINE CASCADE;
DROP VIEW IF EXISTS COMBINE2 CASCADE;
DROP VIEW IF EXISTS COMBINE3 CASCADE;
DROP VIEW IF EXISTS ANSWER CASCADE;

--Determine all cabinets that were formed from 1999.
--所以是选用cabinet_party里的party
CREATE VIEW recentCabParty AS SELECT country_id, party_id, cabinet_id FROM cabinet, cabinet_party
WHERE EXTRACT(YEAR FROM start_date) >= 1999 AND cabinet.id = cabinet_party.cabinet_id;

--All possible party cabinet combinations
CREATE VIEW ShouldHaveBeen AS
SELECT party.country_id, party.id AS party_id, cabinet.id AS cabinet_id
FROM party, cabinet WHERE party.country_id = cabinet.country_id;


--Remove repetition of parties that have never been committed
CREATE VIEW notcommittedParty AS SELECT DISTINCT party_id AS id
FROM ((SELECT * FROM ShouldHaveBeen) EXCEPT ALL (SELECT * FROM recentCabParty)) AS tempname2;


--Determine committed parties with country id and party name
CREATE VIEW COMBINE AS
SELECT country_id, party.id AS party_id, party.name AS partyName
FROM party, ((SELECT id FROM party) EXCEPT (SELECT id FROM notcommittedParty)) AS tempname
WHERE party.id = tempname.id;

--Add more details to the table.
CREATE VIEW COMBINE2 AS
SELECT country_id, COMBINE.party_id, partyName, family
FROM COMBINE LEFT JOIN party_family ON party_family.party_id = COMBINE.party_id;



CREATE VIEW COMBINE3 AS
SELECT country_id, COMBINE2.party_id, partyName, family, state_market
FROM COMBINE2 LEFT JOIN party_position ON party_position.party_id = COMBINE2.party_id;



CREATE VIEW ANSWER AS
SELECT country.name AS countryName, partyName, family, state_market
FROM COMBINE3, country WHERE country_id = country.id;


INSERT INTO q3
SELECT countryName, partyName, family AS partyFamily, state_market AS stateMarket
FROM ANSWER;