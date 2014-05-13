import os
import psycopg2
from datetime import datetime
from urlparse import urlparse

conn = psycopg2.connect(os.environ["DATABASE_URL"])
print "Opened database successfully"

cur = conn.cursor()

"""
cur.execute("INSERT INTO pinterest (ID, request_time, url, domain, pin_count) VALUES (DEFAULT, %s , %s, %s, %s);", (datetime.now(), 'http://allrecipes.com', 'allrecipes.com', 66))
conn.commit()
print 'Records created'

cur.execute("INSERT INTO facebook (ID, request_time, url, domain, share_count, comment_count, like_count) VALUES (DEFAULT, %s , %s, %s, %s, %s, %s);", (datetime.now(), 'http://allrecipes.com', 'allrecipes.com', 45, 23, 111))
conn.commit()

conn.close()
"""



"""
DROP TABLE pinterest;

CREATE TABLE pinterest (
  id SERIAL PRIMARY KEY NOT NULL,
  request_time TIMESTAMP NOT NULL,
  url VARCHAR(200) NOT NULL,
  domain VARCHAR(60),
  pin_count INTEGER,
  ip_address CIDR
);

CREATE INDEX pinterest_domain_index ON pinterest (domain);

CREATE INDEX pinterest_url_index ON pinterest (url);

--------------------------

CREATE TABLE twitter (
  id SERIAL PRIMARY KEY NOT NULL,
  request_time TIMESTAMP NOT NULL,
  url VARCHAR(200) NOT NULL,
  domain VARCHAR(60),
  share_count INTEGER,
  ip_address CIDR
);

CREATE INDEX twitter_domain_index ON twitter (domain);

CREATE INDEX twitter_url_index ON twitter (url);

---------------------------

CREATE TABLE google (
  id SERIAL PRIMARY KEY NOT NULL,
  request_time TIMESTAMP NOT NULL,
  url VARCHAR(200) NOT NULL,
  domain VARCHAR(60),
  share_count INTEGER,
  ip_address CIDR
);

CREATE INDEX google_domain_index ON google (domain);

CREATE INDEX google_url_index ON google (url);

---------------------------

CREATE TABLE facebook (
  id SERIAL PRIMARY KEY NOT NULL,
  request_time TIMESTAMP NOT NULL,
  url VARCHAR(200) NOT NULL,
  domain VARCHAR(60),
  share_count INTEGER,
  comment_count INTEGER,
  like_count INTEGER,
  ip_address CIDR
);

CREATE INDEX facebook_domain_index ON facebook (domain);

CREATE INDEX facebook_url_index ON facebook (url);


"""










