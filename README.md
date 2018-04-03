# News Report Tool
  - This is a small program in **Python**. When running this program, it will  
    generate a text file with data analysis for the news website
  - The database used for this news website is PostgreSQL

# Environment
  - **Python** with version 2.7
  - Follow this [guidance](https://www.python.org/about/gettingstarted/) to install Python on your operating system.
  - Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html)

# How to Run
  - Downloads the Vagrant Config File [Here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f73b_vagrantfile/vagrantfile)
  - run the following command
  ```
  $ vagrant up
  $ vagrant ssh
  ```
  - downloads the news website data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)  
  - run the following command
  ```
  $ cd /vagrant
  $ psql -d news -f newsdata.sql
  ```
  - The VM and database is set up, now you can run the python file using:
  ```
  $ python tool.py
  ```

# PostgreSQL requirement
  - Run thefollowing command on the PostgreSQL shell to create the views so that the python code can run properly
  ```sql
  create view pageviews as
  select path, count(*) as num
  from log where path != '/'
  group by path
  order by num desc;

  create view author_articles as
  select authors.name, articles.slug
  from authors, articles
  where authors.id = articles.author;

  create view date_status as
  select time::date as date, status
  from log
  order by time;

  create view date_errors as
  select date, count(*) as errors
  from date_status where status != '200 OK'
  group by date
  order by date;

  create view date_views as
  select date, count(*) as views
  from date_status
  group by date
  order by date;

  create view date_views_errors as
  select date_views.date, date_views.views, date_errors.errors
  from date_views, date_errors
  where date_views.date = date_errors.date;
  ```
