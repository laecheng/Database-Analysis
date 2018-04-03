#!/usr/bin/env python
# coding: utf-8
# A report tool that generate report from a news database

import psycopg2


def analyze_data(query):
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    return rows

if __name__ == '__main__':
    report_file = open("report.txt", "wb")
    report_file.write("1. What are the most popular three articles of" +
                      " all time?\n")
    query = """
            select title, num from articles, pageviews
            where path = '/article/' || articles.slug
            order by num desc limit 3;
            """
    for rows in analyze_data(query):
        report_file.write("\"" + rows[0] + "\"" + " —— " + str(rows[1]) +
                          " views\n")

    report_file.write("\n2. Who are the most popular article authors of" +
                      " all time?\n")
    query = """
            select name, sum(num) as sum from author_articles, pageviews
            where path = '/article/' || slug group by name order by sum desc;
            """
    for rows in analyze_data(query):
        report_file.write(rows[0] + " —— " + str(rows[1]) + " views\n")

    report_file.write("\n3. On which days did more than 1% of requests lead" +
                      "to errors? \n")

    query = "select date from date_views_errors where errors * 100 > views"
    for row in analyze_data(query):
        report_file.write(str(row[0]) + "\n")

    report_file.close()
