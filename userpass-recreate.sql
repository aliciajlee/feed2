drop table if exists Users;

create table Users(
       uid int auto_increment,
       username varchar(50) not null,
       hashed char(60),
       unique(username),
       index(username),
       primary key (uid)
);
