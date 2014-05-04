import requests
from socialanalytics import pinterest, facebook
import json
import pytz
from datetime import timedelta, datetime
from flask import Flask, url_for, request, jsonify, render_template, make_response, current_app 
from werkzeug import SharedDataMiddleware
from functools import update_wrapper


app = Flask(__name__)


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
@app.route('/')
def root():
    return render_template("index.html")

"""
@app.route('/')
def api_root():
    return 'Welcome to SocialAnalytics'
"""


@app.route('/api/v1/pinterest')
@crossdomain(origin='*')
def api_pinterest():
    if 'url' in request.args:
        url = request.args['url']
        pins = pinterest.getPins(url)
        if type(pins) == int:
            pin_dict = { 'timestamp': get_time(),
                    'pin_count': pins,
                    'url': url,
                    'cached': False }

            return jsonify(pin_dict)
        else:
            #return error
            return jsonify({ 'error': pins})
    else:
        return jsonify({ 'error': 'No URL parameter'})


@app.route('/api/v1/facebook')
@crossdomain(origin='*')
def api_facebook():
    if 'url' in request.args:
        url = request.args['url']
        fb_dict = facebook.getObject(url)
        if 'error' not in fb_dict:
            fb_dict['timestamp'] = get_time()
            fb_dict['url'] = url
            fb_dict['cached'] = False

            return jsonify(fb_dict)
        else:
            #return error
            return jsonify(fb_dict)
    else:
        return jsonify({ 'error': 'No URL parameter'})







#### Functions ####
def get_time():
    timestamp = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp




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







