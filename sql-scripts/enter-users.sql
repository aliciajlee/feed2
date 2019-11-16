load data local INFILE
'../starter-data/accounts-list.csv'
into Table Users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';