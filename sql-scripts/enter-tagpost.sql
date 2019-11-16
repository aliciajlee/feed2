load data local INFILE
'../starter-data/tagposts.csv'
into Table Tagpost
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';