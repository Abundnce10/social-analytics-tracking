import os
import requests
from socialanalytics import pinterest, facebook, twitter, google_plus
import json
import pytz
from datetime import timedelta, datetime
from flask import Flask, url_for, request, jsonify, render_template, make_response, current_app 
from werkzeug import SharedDataMiddleware
from functools import update_wrapper
from urlparse import urlparse
import psycopg2


app = Flask(__name__)

conn = psycopg2.connect(os.environ["DATABASE_URL"])
print "Opened database successfully"
cur = conn.cursor()


### Cross Domains ###
def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):  
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



#### Routes ####
"""
@app.route('/')
def root():
    return render_template("index.html")
"""

@app.route('/')
def api_root():
    return 'Welcome to SocialAnalytics'



@app.route('/api/v1/pinterest')
@crossdomain(origin='*')
def api_pinterest():
    if 'url' in request.args:
        url = request.args['url']
        parsed_url = urlparse(url)
        url = remove_params(url).lower()


        # Check if domain is over limit
        #cur.execute("SELECT * FROM pinterest WHERE domain = %s ORDER BY request_time DESC;", (parsed_url.netloc, ))


        # Check if page was searched in the past 24 hours
        cur.execute("SELECT * FROM pinterest WHERE url = %s ORDER BY request_time DESC;", (url, ))
        rowcount = cur.rowcount
        if rowcount > 0:
            row = cur.fetchone()
            time_diff = datetime.now() - row[1]
            # Return cached value if requested in previous 24 hours
            if time_diff.days < 1:
                pins_dict = {
                    'cached': True,
                    'row_count': rowcount,
                    'pin_count': row[4],
                    'request_time': convert_time(row[1]),
                    'url': url
                }
                
                return jsonify(pins_dict)
        


        # Hit Pinterest API
        pins_dict = pinterest.getPins(url)
        if 'error' not in pins_dict:
            pins_dict['request_time'] = convert_time(datetime.now())
            pins_dict['url'] = url
            pins_dict['cached'] = False

            # Save result to database
            cur.execute("INSERT INTO pinterest (ID, request_time, url, domain, pin_count) VALUES (DEFAULT, %s , %s, %s, %s);", (datetime.now(), url, parsed_url.netloc, pins_dict['pin_count']))
            conn.commit()
            print 'Record created'
            
            # Return JSON
            return jsonify(pins_dict)
        else:
            try:
                #Return Error Message
                return jsonify({ 'error': pins_dict['error'] })
            except:
                return jsonify({ 'error': 'Trouble connecting to API. Please try again.' })
    else:
        # Return Error
        return jsonify({ 'error': 'No URL parameter'})




@app.route('/api/v1/facebook')
@crossdomain(origin='*')
def api_facebook():
    if 'url' in request.args:
        url = request.args['url']
        parsed_url = urlparse(url)
        url = remove_params(url).lower()


        # Check if domain is over limit


        # Check if page was searched in the past 24 hours
        cur.execute("SELECT * FROM facebook WHERE url = %s ORDER BY request_time DESC;", (url, ))
        rowcount = cur.rowcount
        if rowcount > 0:
            row = cur.fetchone()
            time_diff = datetime.now() - row[1]
            # Return cached value if requested in previous 24 hours
            if time_diff.days < 1:
                fb_dict = {
                    'cached': True,
                    'row_count': rowcount,
                    'share_count': row[4],
                    'comment_count': row[5],
                    'like_count': row[6],
                    'request_time': convert_time(row[1]),
                    'url': url
                }
                print "returning cached value"
                return jsonify(fb_dict)



        # Hit Facebook API
        fb_dict = facebook.getObject(url)
        if 'error' not in fb_dict:
            fb_dict['timestamp'] = convert_time(datetime.now())
            fb_dict['url'] = url
            fb_dict['cached'] = False

            # Save result to database
            cur.execute("INSERT INTO facebook (ID, request_time, url, domain, share_count, comment_count, like_count) VALUES (DEFAULT, %s , %s, %s, %s, %s, %s);", (datetime.now(), url, parsed_url.netloc, fb_dict['share_count'], fb_dict['comment_count'], fb_dict['like_count']))
            conn.commit()
            print 'Record created'

            return jsonify(fb_dict)
        else:
            try:
                #return error
                return jsonify({ 'error': fb_dict['error'] })
            except:
                return jsonify({ 'error': 'Trouble connecting to API. Please try again.' })
    else:
        return jsonify({ 'error': 'No URL parameter'})





@app.route('/api/v1/twitter')
@crossdomain(origin='*')
def api_twitter():
    if 'url' in request.args:
        url = request.args['url']
        parsed_url = urlparse(url)
        url = remove_params(url).lower()


        # Check if domain is over limit


        # Check if page was searched in the past 24 hours
        cur.execute("SELECT * FROM twitter WHERE url = %s ORDER BY request_time DESC;", (url, ))
        rowcount = cur.rowcount
        if rowcount > 0:
            row = cur.fetchone()
            time_diff = datetime.now() - row[1]
            # Return cached value if requested in previous 24 hours
            if time_diff.days < 1:
                shares_dict = {
                    'cached': True,
                    'row_count': rowcount,
                    'share_count': row[4],
                    'request_time': convert_time(row[1]),
                    'url': url
                }
                print "returning cached value"
                return jsonify(shares_dict)


        # Hit Twitter API
        shares_dict = twitter.getShares(url)
        if 'error' not in shares_dict:
            shares_dict['timestamp'] = convert_time(datetime.now())
            shares_dict['url'] = url
            shares_dict['cached'] = False

            # Save result to database
            cur.execute("INSERT INTO twitter (ID, request_time, url, domain, share_count) VALUES (DEFAULT, %s , %s, %s, %s);", (datetime.now(), url, parsed_url.netloc, shares_dict['share_count']))
            conn.commit()
            print 'Record created'

            return jsonify(shares_dict)
        else:
            try:
                #return error
                return jsonify({ 'error': shares_dict['error'] })
            except:
                return jsonify({ 'error': 'Trouble connecting to API. Please try again.' })
    else:
        return jsonify({ 'error': 'No URL parameter'})



@app.route('/api/v1/google-plus')
@crossdomain(origin='*')
def api_google_plus():
    if 'url' in request.args:
        url = request.args['url']
        parsed_url = urlparse(url)
        url = remove_params(url).lower()


        # Check if domain is over limit


        # Check if page was searched in the past 24 hours
        cur.execute("SELECT * FROM google WHERE url = %s ORDER BY request_time DESC;", (url, ))
        rowcount = cur.rowcount
        if rowcount > 0:
            row = cur.fetchone()
            time_diff = datetime.now() - row[1]
            # Return cached value if requested in previous 24 hours
            if time_diff.days < 1:
                plus_ones_dict = {
                    'cached': True,
                    'row_count': rowcount,
                    'plus_count': row[4],
                    'request_time': convert_time(row[1]),
                    'url': url
                }
                print "returning cached value"
                return jsonify(plus_ones_dict)


        # Hit Google+ API
        plus_ones_dict = google_plus.getPlusOnes(url)
        if 'error' not in plus_ones_dict:
            plus_ones_dict['timestamp'] = convert_time(datetime.now())
            plus_ones_dict['url'] = url
            plus_ones_dict['cached'] = False

            # Save result to database
            cur.execute("INSERT INTO google (ID, request_time, url, domain, share_count) VALUES (DEFAULT, %s , %s, %s, %s);", (datetime.now(), url, parsed_url.netloc, plus_ones_dict['plus_count']))
            conn.commit()
            print 'Record created'

            return jsonify(plus_ones_dict)
        else:
            try:
                #return error
                return jsonify({ 'error': plus_ones_dict['error'] })
            except:
                return jsonify({ 'error': 'Trouble connecting to API. Please try again.' })
    else:
        return jsonify({ 'error': 'No URL parameter'})




#### Functions ####
def convert_time(d):
    return d.strftime('%Y-%m-%d %H:%M:%S')

def remove_params(url):
    if url.find("?") >= 0:
        stop = url.find("?")
        return url[:stop]
    else:
        return url









#### Exploration Routes ####
@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'

@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


@app.route('/names')
def api_names():
    return jsonify({ 'name': 'Jordan' })


@app.route('/json')
def api_json():
    r = requests.get('http://www.json-generator.com/j/bRwOgfpgya?indent=4')
    return json.dumps(r.json())


@app.route('/time')
def api_time():
    return jsonify({ 'timestamp': get_time() })




if __name__ == "__main__":
    if app.debug:
       app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': static_folder
        })
    app.run(debug=True, use_debugger=True, use_reloader=True)







