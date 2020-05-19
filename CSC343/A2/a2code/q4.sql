-- Sequences

SET SEARCH_PATH TO parlgov;
drop table if exists q4 cascade;

-- You must not change this table definition.

CREATE TABLE q4(
        countryName VARCHAR(50),
        cabinetId INT, 
        startDate DATE,
        endDate DATE,
        pmParty VARCHAR(100)
);

/*
pmParty information be not avaliable when 
the pm is false for all parties in one cabinet, 
we don’t know the info of pm.
只有cabinet_party里有pm的信息
*/

DROP VIEW IF EXISTS update_Cabinet CASCADE;
DROP VIEW IF EXISTS StartEndDate CASCADE;
DROP VIEW IF EXISTS MissingPM CASCADE;
DROP VIEW IF EXISTS WithPM CASCADE;
DROP VIEW IF EXISTS answer CASCADE;

--Determine party_id
--因为我们只要pmParty的名字，所以这些party只可能是在cabinet_party里的，普通的party就不用考虑了
CREATE VIEW update_Cabinet AS
SELECT cabinet.id AS cabinet_id, start_date, previous_cabinet_id AS prev_id, cabinet_party.party_id
FROM cabinet_party, cabinet
WHERE cabinet.id = cabinet_party.cabinet_id;


--The end date of each cabinet is the start_date of next cabinet
CREATE VIEW StartEndDate AS
SELECT DISTINCT c2.cabinet_id AS cab_id, c2.start_date AS c2_start_date, c1.start_date AS c2_end_date  
FROM update_Cabinet c1, update_Cabinet c2 
WHERE c1.prev_id = c2.cabinet_id;


--Determine cabinets with missing pm information
--因为只有cabinet_party里的才可能有pm information
CREATE VIEW MissingPM AS
SELECT id AS cabinet_id, start_date, c2_end_date AS end_date, country_id
FROM  cabinet LEFT JOIN StartEndDate ON cab_id = id;


--Combine cabinets that have pm information with  don't
CREATE VIEW WithPM AS
SELECT MissingPM.cabinet_id, start_date, end_date, country_id, party_id
FROM MissingPM LEFT JOIN cabinet_party ON MissingPM.cabinet_id = cabinet_party.cabinet_id
WHERE pm = TRUE or pm is NULL;


--Determine country name and party name according the ids.
CREATE VIEW answer AS
SELECT country.name AS countryName, cabinet_id AS cabinetId, start_date AS startDate, end_date AS endDate, party.name AS pmParty
FROM WithPM, country, party
WHERE country.id = WithPM.country_id AND party.id = WithPM.party_id;

INSERT INTO q4
SELECT countryName, cabinetId, startDate, endDate, pmParty
FROM answer;
