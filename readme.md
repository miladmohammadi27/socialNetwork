# Proposal:
** this project is prototype and could be more optimized forever **

** postman API document is added to project, import it to postman app **


the relational database was not good for this project, because of structure that we
should implement, and scale of this project that have to implement for huge amount 
of requests for example we should create this schema:

tables:

`users`

`post`

`comment`

`likes`

if we have 1M user and each user have 10 post in average,
number of posts equals to 10M and if we want to retrieve one post ,
the database should search in 1M user to find user and then search for users posts in
10M posts, this scenario may cause huge processes for server so this solution for this project 
is not good

-----------------
the implemented solution for this project is use combining of nosql database 
like mongo and relational database together in this structure

`accounts` --> in relational database for authentications(jwt with OTP is implemented)

`profiles` --> in mongo db for storing user profile data such as user profile information,
posts that user has shared, comments on posts, posts likes 

all entities for user such as `post`, `comment`, `likes` are stored in key value dictionary in profiles

benefit of this structure is, if we have 1M user and want to retrieve some user posts it just needs to 
find user profile object_id and find it in mongo then we have access to all entity of user 
without any further connection to database, and also used field for searching in database is
id and _id, that is more efficient than other fields


# How Run & Test:
1- `clone project`

2- `docker-compose up`

3- `create user1 (API)`

4- `create post for user1 (API)`

5- `create user2 (API)`

6- `use API for list all user to find user1's id (API)`

7- `retrieve user1's profile and id for post (API)`

8- `let comment on user1's post (API)`

9- `like user1's post (API)`

10- `retrieve user1's profile and see the result (API)`








