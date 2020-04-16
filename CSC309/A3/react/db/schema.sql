--- load with 
--- sqlite3 database.db < schema.sql

PRAGMA foreign_keys = ON;

drop table if exists user;
drop table if exists achievement;

create table user(
	username varchar(50) primary key,
	password varBINARY(64) not null,
	firstname varchar(50) not null,
	gender varchar(10) not null default 'male',
	email varchar(50) not null,
	creattime timestamp(0) default current_timestamp
);

create table achievement (
  scoreid varchar(100) primary key,
  username varchar(50),
  kill int default 0 not null,
  damage int default 0 not null,
  FOREIGN KEY(username) references user(username) ON DELETE CASCADE
);

---mock users
INSERT INTO user(username,password,firstname, gender,email) VALUES ('user1', '123456', 'Mavis', 'female', 'ok@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user2', '3drh234ur2', 'John', 'male', 'ok@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user3', 'ed2o38asd', 'David', 'female', 'ok@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user4', '1deduh39', 'Arnold', 'unknown', 'ok@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user5', '1ddcvd', 'Cici', 'male', 'ok@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user6', '1dqwdh39', 'Joey', 'female', 'afcek@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user7', '1acwrg9', 'Jack', 'male', 'oaaaaaa@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user8', '1wefffuh39', 'Kylie', 'unknown', 'efwev3@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user9', '1dsscve9', 'Kyle', 'male', 'osv2sdv@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user10', '1sfhyrg', 'Jake', 'male', 'sfe4w@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user11', '1sjceqrg', 'Stan', 'male', 'stan@gmail.com');
INSERT INTO user(username,password,firstname,gender,email) VALUES ('user12', '1sjbx2rg', 'Wendy', 'female', 'wendy@gmail.com');

---mock achievements
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user183974', 'user1', 4, 263);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('userewuf74','user1', 55, 382);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user303224','user3', 52, 246);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user457374','user4', 23, 67);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user111111','user2', 45, 63);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user222222','user3', 38, 86);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user333333','user1', 97, 339);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user444444','user4', 86, 93);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('userd39823','user5', 184, 93);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user392823','user6', 56, 35);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('user308732','user6', 56, 35);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('usexdkw9dy','user7', 35, 78);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('users382kd','user8', 29, 57);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('usee8d3s92','user9', 84, 268);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('usexdkw83w','user10', 92, 47);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('ussdiwue22','user11', 79, 77);
INSERT INTO achievement(scoreid, username, kill, damage) VALUES ('cds827d7jw','user12', 28, 89);
