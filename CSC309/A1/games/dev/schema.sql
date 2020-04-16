
create table appuser (
	userid varchar(50) primary key,
	password varchar(50) NOT NULL,
	gender CHAR(10),
	birthday DATE,
	gift varchar(20),
	subscribe CHAR(10)
);

insert into appuser values('auser', 'apassword', 'male', '2017-03-14', 'nogift', 'yes');
insert into appuser values('jill123', '123456', 'female', '2020-06-14', '3sub', 'no');
insert into appuser values('jack77', 'zxcvbnm', 'male', '2009-09-24', 'giftcard', 'yes');
insert into appuser values('david', 'spiderman', 'male', '1997-12-11', '3sub', 'no');
insert into appuser values('testuser6', 'testpsw', 'female', '2007-01-29', 'nogift', 'yes');
insert into appuser values('cathy13', 'hello', 'female', '2005-04-14', 'giftcard', 'no');
insert into appuser values('jianhao', '123456', 'male', '2005-04-14', 'giftcard', 'no');


create table GuessGame (
	gameid varchar(50) primary key,
	userid varchar(50) NOT NULL,
	moves INT,
	sec INT);

insert into GuessGame values('jianhao89475', 'jianhao', 4, 16);
insert into GuessGame values('jill12324571', 'jill123', 8, 32);
insert into GuessGame values('testuser2143', 'testuser2', 2, 5);
insert into GuessGame values('david356972', 'david', 3, 10);


create table PegSolitare (
	gameid varchar(50) primary key,
	userid varchar(50) NOT NULL,
	moves INT,
	sec INT
);

insert into PegSolitare values('jianhao89475', 'jianhao', 5, 26);
insert into PegSolitare values('jill12324571', 'jill123', 8, 32);
insert into PegSolitare values('testuser2143', 'testuser2', 9, 35);
insert into PegSolitare values('david356972', 'david', 6, 20);
insert into PegSolitare values('xxcocoymlxx8372', 'xxcocoymlxx', 7, 22);

create table PuzzleGame (
	gameid varchar(50) primary key,
	userid varchar(50) NOT NULL,
	moves INT,
	sec INT
);

insert into PuzzleGame values('jianhao89475', 'jianhao', 25, 126);
insert into PuzzleGame values('jack774571', ' jack77 ', 32, 158);
insert into PuzzleGame values('jianhao2143', 'jianhao', 20, 78);
insert into PuzzleGame values('david356972', 'david', 17, 39);
insert into PuzzleGame values('xxcocoymlxx8372', 'xxcocoymlxx', 29, 112);

create table MasterMind (
	gameid varchar(50) primary key,
	userid varchar(50) NOT NULL,
	moves INT,
	sec INT
);

insert into MasterMind values('jianhao89475', 'jianhao', 7, 134);
insert into MasterMind values('jianhao82376', 'jianhao', 10, 192);
insert into MasterMind values('jianhao82322', 'jianhao', 10, 192);
insert into MasterMind values('jianhao83873', 'jianhao', 6, 84);


insert into MasterMind values('jack774571', ' jack77 ', 10, 178);
insert into MasterMind values('jianhao2143', 'jianhao', 5, 99);
insert into MasterMind values('auser154672', 'auser', 9, 76);
insert into MasterMind values('david97372', 'david', 8, 112);