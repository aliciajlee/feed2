-- load data local INFILE
-- '../starter-data/posts.csv'
-- into Table Posts
-- FIELDS TERMINATED BY ','
-- LINES TERMINATED BY '\n';

insert into Posts(pid, uid, pname, rating, price, review, restaurant, location, imgPath, time) values
(1, 1, "Best Spaghetti Carbonara!", "5", "2", "Carmelina's Spaghetti carbonara is the best in Boston (ever since a trip to Rome, I've been on a massive carbonara hunt--and have found nothing as good as in Italy but this is the best it gets in Boston!)","Carmelina's", "Boston", "images/1/1.jpg", "2019-11-16 01:16:08"),
(2, 3, "Korean TAcos", "5", "2", "This place really blew me away! We got the Coreanos Bowl with beef, Kimchi Fritas with Kalbi, one Miso Chicken taco, and one Sweet Bulgogi taco. The Coreanos Bowl and Kimchi Fritas were SO good, would definitely recommend.", "Coreanos Allston", "Allston", "images/3/2.jpg", "2019-11-16 01:23:18"),
(3, 3, "Crispy Chicken Pad Thai", "3", "2", "I liked their pad thai...I didn't think it was that great when I first ate it. It tasted just like any other pad thai that you would get..", "Lemon Thai", "Wellesley", "images/3/8.jpg", "2019-11-18 01:49:37"),
(4, 3, "yummy cannoli", "4", "1", "I got a pistachio cannoli and the ricotta was so rich and creamy, I felt like I was done after a few bites. You can definitely share and I wish I would have. Don't get me wrong though, it's delicious but you think you've had enough after a few bites.", "Mike's Pastry", "300 Hanover St. Boston, MA", "images/3/3.jpg", "2019-11-16 02:33:11"),
(5, 1, "Hummus", "5", "2", "Juniper has the best hummus! I've been to Juniper many times and we always start off by sharing some of the hummus dips. It comes with warm pita bread too.", "Juniper", "Wellesley", "images/1/4.jpg", "2019-11-17 08:31:21"),
(6, 4, "korean street food", "5", "1", "50/50 hotdog: SO YUMS. CHEESUS CHRIST. I was kinda skeptical in getting it sugar coated when they asked but the sugar is not overpowering, it gives the perfect crunch!!! BUNGEOPPANG fish pastries are soft and filling! Pastry-wise it's crispy on the outside, and the inside it's soft and chewy like mochi!", "JSJ Street Kitchen", "Cupertino, CA", "images/4/7.jpg","2019-11-18 01:41:58"),
(7, 1, "mediocre crab cake", "3", "3", "Crab cake combo was shockingly tiny with three tiny, overcooked and over salted shrimps and a bed of lettuce soaked in dressing.", "Legal Sea Foods", "255 State St. Boston, MA", "images/1/5.jpg", "2019-11-16 09:09:12"),
(8, 1, "Pastries", "5", "2", "Simply just look at their high quality artisanal crafted croissants! My favorites are their pistachios and almond croissants. They even stay crispy even over several days in the fridge.", "Tatte", "Boston", "images/1/6.jpg", "2019-11-17 02:50:11"),
(9, 4, "poke", "5", "2", "My pick of protein is salmon topped with pineapple, cilantro, edamame, crispy garlic and avocado and infused altogether with their ponzu and spicy sauce. The portion was on the smaller side; nevertheless, everything in the bowl was packed with flavor. The fish was chunky and clean tasting. The avocado was fresh and worth the $1 extra. Also, the crunchy toppings was a nice touch.", "Poké Bar", "San Jose, CA", "images/4/9.jpg", "2019-11-18 01:47:17"),
(10, 5,"Strawberry Bingsoo", "4", "2", "Ordered the Fresh Strawberry, and it was so smooth and light! Literally melts in your mouth. It wasn't too sweet at all, and the mochi was perfectly chewy.", "Sul & Beans", "Cupterino, CA", "images/5/10.jpg", "2019-11-24 03:19:47"),
(11, 1, "Sake maguro hamachi don", "5", "2", "I've only ever had take out but the quality is amazing so I can only imagine what dining in will be like (one day!). Had the Sake Maguro Don (salmon, blue fin tuna, & yellowtail - 3 of my favorite fish) and added flying fish roe because you can never have enough roe! Generous portions & beautiful cuts of fish that are incredibly fresh. Sushi rice is done right and so is that ratio of rice to fish. Highly recommend. Looking forward to a sit down meal there one day!", "Tora", "Boston", "images/1/11.jpg", "2019-11-24 03:24:14"),
(12, 4, "Ricotta Jam Tartine", "4", "2", "This toast hits the spot when you're craving something sweet and creamy, but not too rich. The cruncy texture of the toast balanced out with the tangy, creamy ricotta and the sweetness of the jam.", "Tatte", "Boston", "images/4/12.jpg", "2019-11-25 14:41:17"),
(13, 4, "Dougie", "4", "2", "This isn't your everyday pizza - toppings on the Dougie include potato, creamy dressing, and garlic! It makes for a great savory pizza with delightfully chewy crust and a whole lot of flavor. So good!", "Oath Pizza", "Cambridge, MA", "images/4/13.jpg", "| 2019-11-25 14:56:34"),
(16, 11, "Strawberry Kakigori", "5", "3", "delicious, fresh, great on a hot summer day", "Tokyo Kakigori", "Tokyo", "images/11/13.jpg", "2019-11-24 15:39:11"),
(19, 11, "Salmon Nigiri", "4", "3", "yummy, fresh, marbled salmon.", "Minado", "Natick", "images/11/14.jpg", "2019-11-24 15:45:14"),
(20, 5, "Korean Fried Chicken", "3", "2", "The fried chicken was ok! I actually liked the soy garlic better than the spicy. The spicy wasn't spicy enough for me and it tasted quite bland. I liked it but it wasnt anything special. I'll probably go back to crave in chinatown even if their service is slow.", "Bonchon", "Cambridge", "images/5/20.jpg", "2019-11-25 16:15:57"),
(21, 4, "pan friend dumplings", "5", "2", "best authentic pan fried dumplings. crispy on the outside and so juicy and flavorful!", "Shanghai Garden", "Cupertino", "images/4/21.jpg", "2019-11-25 16:34:42"),
(22, 1, "Torched Salmon Belly", "5", "3", "Torched Salmon Belly with tomato, tahini, sushi rice, and green onions - just watching the prep for this dish alone was mesmerizing! The flavors combinations of the salmon and tahini were super unique and definitely something I've never had before - so good! Everyone should try this at least just once.", "Saltie Girl", "Boston", "images/1/22.jpg", "2019-11-25 16:42:06");
