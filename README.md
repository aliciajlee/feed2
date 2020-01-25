# Feed
# FEED TECHNICAL REPORT
Alicia Lee, Rachel Navarrette, Sandra Xu


# INTRODUCTION
As self-proclaimed foodies, we struggle to find appetizing and aesthetic dishes at restaurants. Many social media applications lack features that make the enjoyment of sharing food photos possible. We found that Pinterest lacked information on where food photos were taken, like restaurant location or what the dish was called. Yelp contains reviews of restaurants only, and not specific dishes served at those restaurants. It lacks that appeal that instagram food shots achieve. It seemed like these social media applications all had features that were needed on one platform. As a result, Feed combines the best of social media (e.g. Instagram, Pinterest, Yelp),such as looking up dish reviews and pricing, and filtering/searching through content, searching through users and their posts.  

# USER GUIDE
Getting started on Feed
Sign up for a Feed account and choose a username that clearly represents your brand
Add a profile photo, display name, a biography. You can edit this and your username at anytime using “edit profile” on your profile page. 
Use tags to connect with your audience, and search users and posts, sort your feed by rating or time stamp, or filter by tag. 
Start sharing photos on Feed, including dish name, review, rating, price, and tags. 
Creating an Account & Username
To create a Feed account from a computer:
Click ‘Create New Account’ then enter your email address, name, username, and enter password twice, then click sign up.
Usernames can only consist of letters (american/english?), numbers, periods (.) and underscores (_) and must be at most 20 characters long. Emails must contain ‘@’ but don’t have to be valid emails. 
If you sign up with email, make sure you enter your email address correctly and choose an email address that only you can access. Usernames are unique, so be aware that you must create a username that is not taken by current users of Feed. 
 
Updating Profile Information
You may need to log into your account before you're able to update your profile information.
To update your profile information, including your username and display name associated with your account:
Go to your profile: 
Click Edit Profile.
Type in your information and click save changes (computer and mobile browser).
Some profile information isn't visible to anyone but you. This includes your email address and password. 
 
Navigating the App
Log in screen
The log in screen lets you create a new account or log into an existing account. 
Keep in mind that when logging into an existing account, you must use the username and password for the account.
Log out screen 
To log out of your account, click on the Logout icon (or go to /logout/).
 
Profile
Profile shows your bio and Feed posts. It's also where you can edit your profile info and adjust your Account Settings.
Get to your profile by clicking. On the web, you can also view your profile by going to /profile/ or /profile<your-username>.
 
Adding, Editing, Deleting, and Viewing Posts
Add button lets upload a photo with information of the dish, and share them in Feed. It is required to fill out all fields. 
Click on a post on your feed and be redirected to /post/<pid>/ that displays information about a specific post (e.g. review, stars, price, etc.). You may also view a post by going to /post/<pid>/.
You may click on the user who posted to redirect to that user’s profile.
You may click on a tag to see other posts with the same tag
 
You can edit or delete a post by clicking on one of your posts. If the post is yours, you will see icons to editand delete the post.
To edit or delete a post:
Click  to edit post. Click  to delete the post. 
Edit your post including dish name, rating, tags. The only field you cannot change is the photo, then click Save Changes. The time posted will remain the same.
By clicking on the delete button, the post will be deleted and will no longer show up on your profile page or the home feed. 
Search 
On  Search you can find users and posts that you might like and want to follow from accounts of other users on Feed. 
Searching: type in a search term in the search form in the navbar and select whether you want to search for users or posts. 
Press ‘enter’ or click the search icon button to complete your search (see example searches below). You may also (for whatever reason) type in your search query @ /search/?query=<query>&type=<type>

Home

Click on  (or go to /home/) on the top left of the navbar to redirect to the home.
Home shows a feed of photos posted by all users on the site.

How Home Feed works?

Feed is a place where you can share and connect with the people and things you care about. When you open Feed or refresh your feed, you will see posts from all the users on Feed. To customize your home feed experience, you can sort by rating or by time stamp.

Activity on home Feed:
Click on a post on your feed (or go to /post/<pid>/ ). Click on to like a post. Click on users hyperlink to see a list of users who liked the post. You may also like your own posts. 


Managing your Followers

To unfollow someone:
Go to the profile of the person you'd like to unfollow.
Click Following to confirm unfollowing.
Once you've unfollowed someone, their profile will say Follow instead of Following.
To follow someone:
Go to the profile of the person you'd like to follow.
Click Followto confirm following.
Once you've followed someone, their profile will say Following instead of Follow.
To see a list of followers and following on a profile page:
Click on followers or following hyperlinks to get the list of users
 
# TECHNICAL DETAILS:
ER diagram 

Tables 

User Table

Uid (int)
Fullname (varchar)
Email (varchar)
Username (varchar)
Hashed (char)
Biotext (varchar)
profpicpath (varchar)

Our User Table holds a unique user id uid that serves as the primary key and is also a foreign key in all other tables that reference the user. We also hold the username set by the user, and their hashed password.
Post Table
pid (int)
uid (int)
dishName (varchar 50)
rating (1, 1.5, 2, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)(only options) 
review (varchar 500)
RestaurantName
filePath 
location (varchar 50)
price (1, 2, 3, 4) (only options)
time(timestamp)
Our Post Table holds a unique post id pid that serves as the primary key and is also a foreign key in all other tables that reference the post. We also have a foreign key uid that references the post author. We also hold the dish name, rating, review, restaurant name, location, and price, which are all inputted by the user when they create the post. The filePath is the location in the file directory where the post image has been saved to. The time is generated once the post is added to the database. 
Tag Table
Tag (str)
tid (int)
The Tag table holds a unique tag id tid that serves as the primary key and is also a foreign key in all other tables that reference the tag. The name of the tag is specified by the ttype.

Likes Table

Post_id (int)
Profile_id (int)
The post_id is a foriegn key that references pid of the Post table. The profile_id is a foriegn key that references the uid of the User table. This keeps track of who likes what post and how many likes there are in a post. 

Follows Table

Follower_id (int)
Followee_id (int)
Follower_id is a foreign key that references uid of the Users table, and Followee_id is a foreign key that references uid of the Users table. This keeps track of who is following who and can keep track of follower and following count for each profile. 
Flask Routes

@app.route('/')
Checks if user is logged in by checking if there is an active session. If they are logged in, redirect to /home/, otherwise direct to signup.html page.

@app.route("/home/")
Home feed displays the name, rating, first 150 chars, and picture of all posts in the the Posts table. Checks if the ‘sort by’ drop down was selected a tag, and if so, redirects to 

@app.route('/tags/<tag>/', methods=["GET"]). Checks if the ‘sort by’ drop down was selected a category to sort by. If ‘most recent’ was selected, gets all the posts from the Posts table, which is assumed to be sorted by most recent. If ‘rating’ was selected, gets all the posts sorted by rating. If no option was selected, default is sort by most recent.

@app.route("/search/", methods=["GET"])
Redirects here when a search was made in the search bar in the navbar. Gets the search query and type (either posts or users) from the search form. If type is posts, gets all posts from the Posts table where post name, post review, restaurant, location, user who posted, or tags match the search query. If type is users, gets all the users from the Users table where username or full name match the search query. Displays these results in the template home.html.

@app.route('/alike/<post>', methods= ["POST", "GET"])   
Adding a like is an ajax function, given the post_id, will add the uid of the session to the Likes table, using addLike(conn, post, session['uid']) . It will recount the number of likes using countLikes(conn, post), returning the new updated number number of likes for that post in a json that javascript can read to automatically increment the count in post.html, without the user reloading the page. The CSS of the like button changes according to whether the button was liked or not (changing it red when the user likes the post, changing it to grey when the user unlikes the post or doesn’t like the post). If an exception is thrown when accessing the database, it returns the json containing the error. 

@app.route('/dlike/<post>', methods= ["POST", "GET"])   
Deleting a like is an ajax function, given the post_id, will delete the post_id in the Likes table where the profile_id equals session’s uid, using removeLike(conn, post, session['uid']). It will recount the number of likes using countLikes(conn, post), returning the new updated number number of likes for that post in a json that javascript can read to automatically increment the count in post.html, without the user reloading the page. It uses a different javascript function than the add like javascript function to post the new updated like when the user decides to unlike a post. The CSS of the like button changes according to whether the button was liked or not (changing it red when the user likes the post, changing it to grey when the user unlikes the post or doesn’t like the post). If an exception is thrown when accessing the database, it returns the json containing the error. 

@app.route('/listofLikes/<post>', methods = ["POST", "GET"])
Using a post_id as a given parameter, it gets a list of all the users who liked a particular post using likesList(conn, pid), using the Likes table.When a user clicks on ‘users’ found in post.html, the hyperlink is redirected to this app route function that gets the list of people who liked, and redirects the user to a new page called listofFollowing.html (badly worded html page, I know, but it is the same template used to get the list of followers and following, hence why it was named that), where the list of users are transferred and processed for formatting.

#display info of an individual post
@app.route('/post/<pid>/')
Displays information of an individual post with the given pid. Gets the name, user who posted, rating, price range, restaurant, location, review, tags, and time posted from the Posts table, and gets the number of likes from the Likes table. Displays these information in the template post.html. Checks if If the user logged in posted the post, and if so, edit and delete buttons will be displayed. Clicking on these buttons will pop up the edit and delete forms. User who posted and tags are links that redirect to @app.route('/profile/<username>')and @app.route('/tags/<tag>/', methods=["GET"])respectively. 

@app.route('/signUp/', methods=["GET","POST"])
When a user is on the signup page (signup.html) and filled all fields and submits the form. It is redirected to this app route. It will be redirected to the signup page if a user is trying to get to the signup page. Otherwise the form is processed, where full name( display name), user, email, and password is found from the form. The profile picture path is a default picture that is found in 'img/default_profilepic.jpeg'. If the passwords don’t match, then the user page is reloaded to the signup page again and needs to fill out the form again. Otherwise, the password is bcrypted (hashed) and uid, fullname, email, username, hashed password, biotext, and profile picture image path, is inserted into the Users table, using '''INSERT INTO Users(uid,fullname,email,username,hashed, biotxt, profpicPath)
                                VALUES(null,%s,%s,%s,%s, null, %s)''',
                            [fullname, email, username, hashed_str, profpicPath]. If an exception is thrown, it is because the username is taken, and the user has to fill in the form again when the page is reloaded. Uid is determined by the last inserted id in the Users table, and the username uid and logged in status and fullname are all stored in a session. Upon signing up, a folder with the user’s unique uid is made and named where their profile picture will live (not the default picture, but whatever picture they decide to upload). If another exception is thrown, it means that not all fields were filled out in the form, and the user must fill out the form again. Upon completion, it will redirect to the user app route, where it will redirect the user to the home feed. 

@app.route('/login/', methods=["GET","POST"])
If user is already logged in, the login page will not show up and will be redirected to the home feed. If the user is not in session, then it will redirect to the login page (login.html). It will take the username and password, and check whether the username is found. If it is, it will process to check the password. Otherwise, an error will flash and the user will have to try logging in again and the login page reloads. The password that the form contains will be hashed and checked whether the password that is found in the Users table that matches that username. If they match, the username, uid, logged in status, full name are stored in a session, otherwise it will flash that username and or/password incorrect, and prompt the user to reattempt login. Otherwise if an exception is thrown, then is will flash that not all fields were filled in and prompt the user to reattempt login.

@app.route('/user/<username>')
From logging in or signing up app routes, given the username, the function gets the session information such as username, uid, fullname. It gets the bio text using getBioText(conn, uid)and getPPic(conn, uid), redirecting the user to home. If the user is not in session, it is prompted to login or join and redirecting to the index page (in this case will be the signup/login page). Otherwise an exception is thrown and flashs the error with redirects to the index app route. 

@app.route('/logout/')
When the log out button is clicked on the navigation bar (in nav.html), it checks whether the user is in session, and pops the username, uid, logged_in status, and redirects to the signup/login page (using index app route). If an exception is thrown, it flashes the error and redirects to the index route. 

@app.route('/upload/', methods=["POST"])
Gets the name, restaurant, location, rating, price, review, tags, and image file from the POSTed modal upload form in nav.html the user has filled out. Adds the name, restaurant, location, rating, price, and review fields into the Post table with insertPost(conn, uid, name, rating, price, review, restaurant, location), which returns the pid of the newly added post. Uses the pid of the newly added post to rename the image file. If this is a user’s first upload, create a folder named their uid. Save the renamed image in the user folder. Adds the filepath of the image into the Post table with insertFilepath(conn, path, pid). Adds each post’s tag into the TagPost table with insertTagPost(conn, pid, tid) and flash that the upload was successful. If the upload fails, flash why the upload failed and let the user try again.

@app.route('/profile/')
Goes to this route when user clicks on the profile icon. Gets the username of the user logged in from the session, and redirects to @app.route('/profile/<username>')

@app.route('/profile/<username>')
Displays information of a user with the given username. Gets the name, bio text, profile picture, number of posts, number of people following the user, number of people the user is following, and all posts made by user from the Users, Follows and Posts table and displays them. If the user logged in is the same as the profile’s user, display the edit profile button. Check if the current user logged in is or is not following the profile’s user, and displays the following button with either ‘follow’ or ‘unfollow’ as its text.

@app.route('/follow/<username>', methods= ["POST"])   
Adding a follow is an ajax function, given the username, it will get the profile id it is on and using the session uid and the profile_id it finds from username, it will use addfollower(conn, session['uid'], profUID)to add that information into the Follows table. It will recount the number of following and number of followers for that profile page using numFollowing(conn, profUID)and numFollowing(conn, profUID). It will store the new numbers in a json that the javascript function in profile.html will read and post to the user without reloading the page. If it catches an error, it will store and return the error in a json for the javascript function to read as well. The button to follow and unfollow does not show up if the profile matches the session’s profile. This is taken care of in the profile.html using jinja2.  

@app.route('/unfollow/<username>', methods= ["POST"])   
Deleting a follow is an ajax function, given the username, it will get the profile id it is on and using the session uid and the profile_id it finds from username, it will use deletefollower(conn, session['uid'], profUID)to delete hat information from the Follows table. It will recount the number of following and number of followers for that profile page using numFollowing(conn, profUID)and numFollowing(conn, profUID). It will store the new numbers in a json that the javascript function in profile.html will read and post to the user without reloading the page. If it catches an error, it will store and return the error in a json for the javascript function to read as well. The button to follow and unfollow does not show up if the profile matches the session’s profile. This is taken care of in the profile.html using jinja2.  

@app.route('/listofFollowers/<username>', methods = ["POST", "GET"])
Using a username as a given parameter, it gets a list of all the users who are followers of the profile with that given username. It gets the profile’s uid and uses followersUsers(conn, profUID), to get the list of followers from the Follows table.When a user clicks on ‘followers’ found in profile.html, the hyperlink is redirected to this app route function that gets the list of people who follower that profile, and redirects the user to a new page called listofFollowing.html, where the list of users are transferred and processed for Bootstrap formatting.

@app.route('/listofFollowing/<username>', methods = ["POST", "GET"])
Using a username as a given parameter, it gets a list of all the users who the profile with that given username is following. It gets the profile’s uid and uses followingUsers(conn, profUID), to get the list of followers from the Follows table.When a user clicks on ‘followers’ found in profile.html, the hyperlink is redirected to this app route function that gets the list of people who that profile is following, and redirects the user to a new page called listofFollowing.html, where the list of users are transferred and processed for Bootstrap formatting.

@app.route('/editprofile/', methods= ["POST", "GET"])   
Gets the username, fullname, bio, and image file (if found) from the POSTed modal upload form in profile.html the user has filled out. Adds the username, fullname, biotext, filePath fields into the Users table with editProfile(conn, uid, username, fullname, biotext, filePath), which updates User information. It first checks whether the filePath image has the allowed extensions of {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}. The profile picture will go into a folder named after their uid where the profile picture is saved. As default before users change their profile picture for the first time, a default picture is set to an avocado. If an image is not provided in the form, then the profile is updated without the filePath indicated so the current profile picture remains intact. In both cases, it redirects to the profile app route.

@app.route('/delete_post/<pid>', methods=['POST'])
Deletes the post with the given pid from the Posts table, and redirects to home.

@app.route('/edit_post/<pid>', methods=['POST'])
Redirects here when the edit post form of post with given pid is submitted. Gets the name, restaurant, location, rating, price, review, and tags from the form and updates these values in the Posts table. Deletes all tags of the post, and inserts all tags that were collected from the form into the Tagpost table.

@app.route('/tags/<tag>/', methods=["GET"])
Fetches the tag name from the url, converts it into its tag id using the Tag table with the getTid(conn,ttype)function and looks up all the posts with the tid using an inner join between the TagPost table and the Post table using the getPostsWithTid(conn, tid)function. Displays the queried posts using the home.html template.

 
# CONCLUSION:
Feed is a fully-functioning food blogger’s social media heaven. Users have the power to share their food experiences with the world using our upload form, discover the latest food trends by viewing posts in a beautiful grid format, and connect with similar-minded foodies by following other accounts and liking their posts.  Join the Feed community of foodies today! 
We promise not to waste your investment with our goal to release IPOs to the market one day. We won’t let you down!
 
# FUTURE DIRECTIONS:
For the future, we hope to deploy the website to the public, and create a mobile application version of the site. We also hope to make it more social, by implementing comments and additional security of accounts by verifying emails, recovering passwords. We want to make the feed and search more robust as the data set expands, by creating the feed for just users that you follow, and to sort by not just rating and time stamp, but also by price. We hope to one day partner with advertisement companies, restaurants, and food delivery companies to monetize the application in the future.  
 
 
 
 
