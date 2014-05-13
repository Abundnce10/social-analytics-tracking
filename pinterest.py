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
conn.close()
"""



"""
CREATE TABLE pinterest (
  id SERIAL PRIMARY KEY NOT NULL,
  request_time TIMESTAMP NOT NULL,
  url VARCHAR(200) NOT NULL,
  domain VARCHAR(60),
  pin_count INTEGER,
  ip_address CIDR
);

CREATE INDEX domain_index ON pinterest (domain);

CREATE INDEX url_index ON pinterest (url);
"""