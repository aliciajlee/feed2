load data local INFILE
'../starter-data/follow-list.csv'
into Table Follows
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';