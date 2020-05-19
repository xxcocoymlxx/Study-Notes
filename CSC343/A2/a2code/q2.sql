-- Participate

SET SEARCH_PATH TO parlgov;
drop table if exists q2 cascade;

-- You must not change this table definition.

create table q2(
        countryName varchar(50),
        year int,
        participationRatio real
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)

DROP VIEW IF EXISTS All_Participation_Ratios CASCADE;
DROP VIEW IF EXISTS Decrease_Countries CASCADE;
DROP VIEW IF EXISTS Target_Countries CASCADE;


--Determine participation ratios of all elctions between 2001 and 2016
CREATE VIEW All_Participation_Ratios AS
SELECT country_id, EXTRACT(YEAR FROM e_date) AS year,
AVG(CAST(votes_cast AS FLOAT)/electorate) AS participation_ratio
FROM election
WHERE e_date >= '2001-01-01' AND e_date <= '2016-12-31'
AND electorate is not null and votes_cast is not null
GROUP BY country_id, EXTRACT(YEAR FROM e_date);

--all countries whose participation ratios were greater in a previous year (not increasing by year)
CREATE VIEW Decrease_Countries AS
SELECT DISTINCT PR1.country_id
FROM All_Participation_Ratios PR1 JOIN All_Participation_Ratios PR2 ON PR1.country_id = PR2.country_id
WHERE PR1.year > PR2.year and PR1.participation_ratio < PR2.participation_ratio;


--Determine the country with non-decreasing paticipation in election.
CREATE VIEW Target_Countries AS
SELECT PR.country_id, year, participation_ratio AS participationRatio,country.name AS countryName
FROM All_Participation_Ratios PR JOIN country ON PR.country_id = country.id
WHERE NOT EXISTS (SELECT * FROM Decrease_Countries DC WHERE PR.country_id = DC.country_id);

-- the answer to the query 
INSERT INTO q2 
SELECT countryName, year, participationRatio 
FROM Target_Countries;