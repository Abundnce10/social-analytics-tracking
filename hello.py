import requests
from socialanalytics import pinterest, facebook
import json
import pytz
import datetime
from flask import Flask, url_for, request, jsonify


app = Flask(__name__)


#### Functions ####
def get_time():
    timestamp = datetime.datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
    return timestamp


#### Routes ####
@app.route('/')
def api_root():
    return 'Welcome to SocialAnalytics'

@app.route('/api/v1/pinterest')
def api_pinterest():
    if 'url' in request.args:
        url = request.args['url']
        pins = pinterest.getPins(url)
        if type(pins) == int:
            obj = { 'timestamp': get_time(),
                    'pin_count': pins,
                    'url': url,
                    'cached': False }

            return jsonify(obj)
        else:
            #return error
            return jsonify({ 'error': pins})
    else:
        return jsonify({ 'error': 'No URL parameter'})

@app.route('/api/v1/facebook')
def api_facebook():
    x = facebook.getObject('http://allrecipes.com/Recipe/Sams-Famous-Carrot-Cake/Detail.aspx')
    return jsonify(x)





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



if __name__ == '__main__':
    app.run(debug=True)






