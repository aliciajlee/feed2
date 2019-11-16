use sxu5_db;

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


create table Follows(
       follower_id int,
       followee_id int,
       foreign key (follower_id) references Users(uid)
           on delete cascade
);

create table Posts(
    pid int auto_increment not null primary key,
    uid int,
    pname varchar(30),
    rating enum("1", "2", "3", "4", "5"),
    price enum ("1", "2", "3", "4"),
    review varchar(500),
    restaurant varchar(30),
    location varchar(50),
    imgPath varchar(50), 
    time timestamp,
    foreign key (uid) references Users(uid)
           on delete cascade        
);

create table Tags(
    tid int auto_increment primary key,
    ttype varchar(20)
);

create table Tagpost(
       pid int,
       tid int,
       foreign key (pid) references Posts(pid)
           on delete cascade,
       foreign key (tid) references Tags(tid)
           on delete cascade
);

-- enter data
source enter-users.sql;
source enter-follows.sql;
source enter-tags.sql;
source enter-posts.sql;
source enter-tagpost.sql;