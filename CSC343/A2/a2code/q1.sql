-- Winners

SET SEARCH_PATH TO parlgov;
drop table if exists q1 cascade;

-- You must not change this table definition.

create table q1(
countryName VARCHaR(100),
partyName VARCHaR(100),
partyFamily VARCHaR(100),
wonElections INT,
mostRecentlyWonElectionId INT,
mostRecentlyWonElectionYear INT
);

-- You may find it convenient to do this for each of the views
-- that define your intermediate steps.  (But give them better names!)
DROP VIEW IF EXISTS maxvotes CASCADE;
DROP VIEW IF EXISTS winner CASCADE;
DROP VIEW IF EXISTS number_win CASCADE;
DROP VIEW IF EXISTS totalwin CASCADE;
DROP VIEW IF EXISTS numberofParties CASCADE;
DROP VIEW IF EXISTS average CASCADE;
DROP VIEW IF EXISTS morethan3 CASCADE;
DROP VIEW IF EXISTS mostrecentelection CASCADE;
DROP VIEW IF EXISTS mostrecentwin CASCADE;
DROP VIEW IF EXISTS d1 CASCADE;
DROP VIEW IF EXISTS d2 CASCADE;
DROP VIEW IF EXISTS d3 CASCADE;
DROP VIEW IF EXISTS answer CASCADE;

--Determine the amount of votes for each elclection's winner. 
--(election_id, party_id) is unique
--所以我们现在是选出一个election里votes最多的那个party
--注意因为这里用了aggregation function，就不可能再同时把party_id选出来
CREATE VIEW maxvotes AS SELECT election_id, MAX(votes) AS winning_votes
FROM election_result GROUP BY election_id; 

--Determine the information of winner party in each election.
--然后只能用我们上面得到的maxvotes来对比得到赢的party和他们的party_id
--从maxvotes,election_result里得到party_id,从election里得到country_id和e_date（所以要join三个）
CREATE VIEW winner AS
SELECT election_result.election_id, country_id, party_id, votes, e_date
FROM (maxvotes JOIN election_result ON maxvotes.election_id = election_result.election_id) 
JOIN election ON election.id = maxvotes.election_id WHERE election_result.votes = winning_votes;


--Determine the total number of wins for each party in every country.
CREATE VIEW number_win AS
SELECT country_id, party_id, COUNT(*) AS won FROM winner GROUP BY country_id, party_id;

--Determine the total number of parties won in each country
CREATE VIEW totalwin AS
SELECT country_id, SUM(won) AS totalwins FROM number_win GROUP BY country_id;

--Determine the number of parties in each country
CREATE VIEW numberofParties AS
SELECT country_id, COUNT(id) AS parties FROM party GROUP BY country_id;

--Determine the average number of elctions won in each country
CREATE VIEW average AS
SELECT totalwin.country_id, CAST(totalwins AS FLOAT)/parties AS average_win
FROM totalwin,numberofParties WHERE totalwin.country_id = numberofParties.country_id;

--Determine all parties that won more than 3 times the average number of elctions in their country.
--report the number of times they won and their perty_id
--这是最重要的一个table，我们最终答案里的其他信息都是根据这里的parties来的
CREATE VIEW morethan3 AS
SELECT number_win.country_id, party_id, won
FROM number_win, average WHERE number_win.country_id = average.country_id AND won > (3*average_win);

--Determine the most recent WIN of each party
--这里记录了most recent win的party
CREATE VIEW mostrecentwin AS
SELECT country_id, party_id, MAX(e_date) AS recent FROM winner GROUP BY country_id, party_id;

--Add the election_id to the mostrecentwin table
--这里记录了每个coutry，party的most recent win的election，之后要从morethan3里配对，之后的table中我们要配上这个election_id
CREATE VIEW mostrecentelection AS
SELECT election_id, mostrecentwin.country_id, mostrecentwin.party_id, recent 
FROM mostrecentwin JOIN winner ON mostrecentwin.country_id = winner.country_id AND mostrecentwin.party_id = winner.party_id
WHERE e_date = recent;

--Add detailed information to the
-- 把每个morethan3里的party找到了这个party most recent win的election_id
CREATE VIEW d1 AS
SELECT morethan3.country_id, morethan3.party_id, won, election_id AS mostrecentId, recent AS mostRecentYear
FROM mostrecentelection,morethan3 WHERE morethan3.party_id =mostrecentelection.party_id;

--把上面得到的每个party配对出对应的Partyfamily
CREATE VIEW d2 AS
SELECT d1.country_id, d1.party_id, won, mostrecentid, mostRecentYear, family
FROM party_family RIGHT JOIN d1 ON d1.party_id = party_family.party_id;

--给上面得到的每个party加上对应的PartyName和CountryName
CREATE VIEW d3 AS
SELECT country.name AS countryName, party.name AS partyName, won, mostrecentid, mostRecentYear, family
FROM d2, country, party WHERE d2.country_id = country.id AND d2.party_id = party.id;


CREATE VIEW answer AS
SELECT countryName, partyName, won AS wonElections, mostrecentid AS mostRecentlyWonElectionId, mostRecentYear AS mostRecentlyWonElectionYear, 
CASE WHEN family != NULL
	 	THEN family
    	ELSE ' '
    	END AS family
FROM d3; 


-- the answer to the query 
insert into q1 
SELECT countryName, partyName, family AS partyFamily, wonElections, mostRecentlyWonElectionId, EXTRACT(YEAR FROM mostRecentlyWonElectionYear)
FROM answer;

