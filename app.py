import json
from flask import Flask, request, jsonify

app = Flask(__name__)


def read_mocked_response():
    with open('mocked_response.json') as json_file:
        response = json.load(json_file)
    return response


def handle_route(**kwargs):
    return jsonify(mocked_response[request.url_rule.rule][request.method]['response']), \
           mocked_response[request.url_rule.rule][request.method]['return_code']


if __name__ == '__main__':
    mocked_response = read_mocked_response()
    for rule in mocked_response:
        app.add_url_rule(rule, 'handle_route', handle_route, methods=list(mocked_response[rule].keys()))
    app.run(host='0.0.0.0')
