-- Alliances

SET SEARCH_PATH TO parlgov;
drop table if exists q5 cascade;

-- You must not change this table definition.

DROP TABLE IF EXISTS q5 CASCADE;
CREATE TABLE q5(
        countryId INT, 
        alliedPartyId1 INT, 
        alliedPartyId2 INT
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS Num_Elections CASCADE;
DROP VIEW IF EXISTS Alliances CASCADE;
DROP VIEW IF EXISTS Num_Alliances CASCADE;
DROP VIEW IF EXISTS ANSWER CASCADE;


--Determine the number of elections in each country
CREATE VIEW Num_Elections AS
SELECT country_id, count(*) AS total_number FROM election GROUP BY country_id;

-- To avoid symmetric pairs (“pseudo-duplicates”) solely include
-- pairs that satisfy alliedPartyId1 <alliedPartyId2.
CREATE VIEW Alliances AS
SELECT e1.election_id AS election_id, e1.party_id AS party1_id, e2.party_id AS party2_id
FROM election_result e1 JOIN election_result e2 ON e1.election_id = e2.election_id
WHERE e1.party_id < e2.party_id AND ((e1.alliance_id = e2.alliance_id) OR (e1.alliance_id = e2.id) OR (e1.id = e2.alliance_id));


--Determine country_id and the amount of each party pair combination has happened
CREATE VIEW Num_Alliances AS
SELECT country_id, party1_id, party2_id, count(DISTINCT election_id) as num_alliances
FROM Alliances, election WHERE election_id = id
GROUP BY party1_id, party2_id, country_id; --distinct combinations of these 3 attributes


--Determine the answer.
CREATE VIEW ANSWER AS
SELECT Num_Alliances.country_id, party1_id, party2_id, num_alliances, (CAST(num_alliances AS float) / total_number) AS ratio
FROM Num_Alliances join Num_Elections on Num_Alliances.country_id = Num_Elections.country_id
WHERE (CAST(num_Alliances AS float) / total_number) >= 0.3;


-- the answer to the query 
INSERT INTO q5 SELECT country_id AS countryId, party1_id AS alliedPartyId1, party2_id AS alliedPartyId2 FROM ANSWER;
