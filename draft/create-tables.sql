
-- CHANGE TO DB NAME
use sxu5_db;


drop table if exists posts;
drop table if exists users;
create table users(
    -- should users have profile pictures?
    uid int auto_increment not null primary key,
    email varchar(30),
    username varchar(20),
    password varchar(20),
    location varchar(30)
);

create table posts (
    pid int auto_increment not null primary key,
    uid int,
    rating enum("1", "2", "3", "4", "5"),
    review varchar(500),
    restaurant varchar(30),
    imgPath varchar(50), 
    location varchar(50),
    price enum ("1", "2", "3", "4"),
    time timestamp,
    foreign key (uid) references users(uid)
        --    on delete cascade
);

drop table if exists tags;
create table tags (
    type varchar(20),
    pid int,
    foreign key (pid) references posts(pid)
           on delete cascade
           on update cascade
);

