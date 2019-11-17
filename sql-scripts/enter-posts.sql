-- load data local INFILE
-- '../starter-data/posts.csv'
-- into Table Posts
-- FIELDS TERMINATED BY ','
-- LINES TERMINATED BY '\n';

insert into Posts(pid, uid, pname, rating, price, review, restaurant, location, imgPath, time) values
(1, 1, "Best Spaghetti Carbonara!", "5", "2", "Carmelina's Spaghetti carbonara is the best in Boston (ever since a trip to Rome, I've been on a massive carbonara hunt--and have found nothing as good as in Italy but this is the best it gets in Boston!)","Carmelina's", "Boston", "images/1/1.jpg", "2019-11-16 01:16:08"),
(2, 3, "Korean TAcos", "5", "2", "This place really blew me away! We got the Coreanos Bowl with beef, Kimchi Fritas with Kalbi, one Miso Chicken taco, and one Sweet Bulgogi taco. The Coreanos Bowl and Kimchi Fritas were SO good, would definitely recommend.", "Coreanos Allston", "Allston", "images/3/2.jpg", "2019-11-16 01:23:18"),
(3, 3, "yummy cannoli", "4", "1", "I got a pistachio cannoli and the ricotta was so rich and creamy, I felt like I was done after a few bites. You can definitely share and I wish I would have. Don't get me wrong though, it's delicious but you think you've had enough after a few bites.", "Mike's Pastry", "300 Hanover St. Boston, MA", "images/3/3.jpg", "2019-11-16 02:33:11"),
(4, 1, "Hummus", "5", "2", "Juniper has the best hummus! I've been to Juniper many times and we always start off by sharing some of the hummus dips. It comes with warm pita bread too.", "Juniper", "Wellesley", "images/1/4.jpg", NOW()),
(5, 1, "mediocre crab cake", "3", "3", "Crab cake combo was shockingly tiny with three tiny, overcooked and over salted shrimps and a bed of lettuce soaked in dressing.", "Legal Sea Foods", "255 State St. Boston, MA", "images/1/5.jpg", NOW()),
(6, 1, "Pastries", "5", "2", "Simply just look at their high quality artisanal crafted croissants! My favorites are their pistachios and almond croissants. They even stay crispy even over several days in the fridge.", "Tatte", "Boston", "images/1/6.jpg", NOW());