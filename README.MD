# The purpose of this code
logproject.py queries the 'news' database (which is made up of 3 tables: articles, authors, and log) to answer 3 questions: 
1. What are the most popular three articles of all time? 
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors? 

# How to run logproject.py
1. Download the file into a folder in vagrant
2. Download the newsdata.sql file
3. ssh into vagrant and manually create the database 'news' 
4. Run `psql -d news -f newsdata.sql` to populate the database with the three tables
5. Create the following views:

```CREATE VIEW statusok AS
SELECT * FROM log 
WHERE status NOT LIKE '404 NOT FOUND' 
AND path LIKE '%/article/%';

CREATE VIEW pathtoslug AS
SELECT substring(statusok.path, 10) AS path, count(*) AS views 
FROM statusok 
GROUP BY path 
ORDER BY views DESC;

CREATE VIEW authorviews AS
SELECT articles.author, sum(pathtoslug.views) AS totalviews 
FROM articles, pathtoslug 
WHERE pathtoslug.path = articles.slug 
GROUP BY articles.author 
ORDER BY totalviews DESC;

CREATE VIEW errordates AS
SELECT CAST(time AS date), status, count(status) AS num 
FROM log WHERE status = '404 NOT FOUND' 
GROUP BY time, status 
ORDER BY num desc;

CREATE VIEW okdates AS
SELECT CAST(time AS date), status, count(status) AS num 
FROM log 
WHERE status = '200 OK' 
GROUP BY time, status 
ORDER BY num desc;

CREATE VIEW ok AS 
SELECT time, sum(num) AS okays 
FROM okdates 
GROUP BY time 
ORDER BY time desc;

CREATE VIEW errors AS 
SELECT time, sum(num) AS errors 
FROM errordates 
GROUP BY time 
ORDER BY errors desc;

CREATE VIEW errorresults AS 
SELECT errors.time, errors/okays AS result 
FROM errors LEFT JOIN ok 
ON errors.time = ok.time;```

6. Navigate to the folder where you downloaded logproject.py and run the file