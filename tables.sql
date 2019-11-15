drop table if exists Follows;
drop table if exists Tagpost;
drop table if exists Tags;
drop table if exists Posts;
drop table if exists Users;

create table Users(
       uid int auto_increment,
       username varchar(50) not null,
       email varchar(50) not null,
       hashed char(60),
       unique(email),
       unique(username),
       index(username),
       primary key (uid)
);

load data local INFILE
'starter-data/accounts-list.csv'
into Table Users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';


create table Follows(
       follower_id int,
       followee_id int,
       foreign key (follower_id) references Users(uid)
           on delete cascade

);

load data local INFILE
'starter-data/follow-list.csv'
into Table Follows
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';



create table Posts(
    pid int auto_increment not null primary key,
    uid int,
    rating enum("1", "2", "3", "4", "5"),
    review varchar(500),
    restaurant varchar(30),
    imgPath varchar(50), 
    location varchar(50),
    price enum ("1", "2", "3", "4"),
    time timestamp,
    foreign key (uid) references Users(uid)
           on delete cascade
           
);


create table Tags(
    ttype varchar(20),
    tid int auto_increment primary key
);

create table Tagpost(
       pid int,
       tid int,
       foreign key (pid) references Posts(pid)
           on delete cascade,
       foreign key (tid) references Tags(tid)
           on delete cascade

);

