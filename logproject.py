#!/usr/bin/env  python2.7

import psycopg2
from datetime import datetime


def connect():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect("dbname=news")


def topThreeArticles():
    """Return top three articles FROM the database."""
    c = connect()
    cursor = c.cursor()
    query = """SELECT articles.title, pathtoslug.views \
    FROM pathtoslug JOIN articles \
    ON pathtoslug.path = articles.slug \
    GROUP BY articles.title, pathtoslug.views \
    ORDER BY pathtoslug.views \
    DESC LIMIT(3);"""
    cursor.execute(query)
    for row in cursor.fetchall():
        print '"%s" - %s Views' % (row[0], row[1],)
    c.close()


def mostViewedArticles():
    """Return most viewed articles"""
    c = connect()
    cursor = c.cursor()
    query = """SELECT authors.name, authorviews.totalviews \
    FROM authors JOIN authorviews \
    ON authors.id = authorviews.author \
    GROUP BY authors.name, authorviews.totalviews \
    ORDER BY authorviews.totalviews DESC;"""
    cursor.execute(query)
    for row in cursor.fetchall():
        print '%s - %s views' % (row[0], row[1],)
    c.close()


def errorDates():
    """Return days where more than 1% of requests lead to errors"""
    c = connect()
    cursor = c.cursor()
    query = """SELECT time, result \
    FROM errorresults \
    WHERE result >= 0.01 \
    ORDER BY time ASC;"""
    cursor.execute(query)
    for row in cursor.fetchall():
        print '%s - %s%% errors' % (row[0].strftime('%B %d, %Y'), round(row[1]*100, 2),)
    c.close()

if __name__ == '__main__':
    topThreeArticles()
    mostViewedArticles()
    errorDates()
