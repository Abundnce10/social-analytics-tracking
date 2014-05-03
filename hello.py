import requests
import json
from flask import Flask, url_for, request, jsonify


app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome to SocialAnalytics'

@app.route('/API/v1/pinterest')
def api_pinterest():
    if 'url' in request.args:
        return 'URL ' + request.args['url']
    else:
        return 'No URL parameter'




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






if __name__ == '__main__':
    app.run(debug=True)






