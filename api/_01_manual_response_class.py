import json
from flask import Flask, Response, abort
from .utils import JSON_MIME_TYPE, search_book
from .utils import json_response, JSON_MIME_TYPE
from flask import request
import requests
from blackfynn import Blackfynn

app = Flask(__name__)

books = [{
    'id': 33,
    'title': 'The Raven',
    'author_id': 1
}]





@app.route('/api/create_session', methods=['GET'])
def session():
    return json_response(json.dumps(books))

# @app.route('/api/create_session', methods=['POST'])
# def sessionp():
#     print(request.method)
#     print(request.headers)
#     print(request.data)
#     print('its a post!')
#
#     r = requests.post("https://api.blackfynn.io/account/api/session", data=request.data)
#
#     print(r.status_code, r.reason)
#     print(r.content)
#     content = r.content
#     response = json.loads(content.decode("utf-8"))
#     global session_id
#     session_id = response['session_token']
#     return json.dumps(response)

@app.route('/api/get_timeseries_dataset_names', methods=['POST'])
def sessionp():
    # print(request.method)
    # print(request.headers)
    # print(request.data)
    # print('its a post!')
    data = json.loads(request.data.decode("utf-8"))
    global bf
    bf = Blackfynn(api_token=data['tokenId'], api_secret=data['secret'])
    data_sets = bf.datasets()

    global time_series_items
    time_series_items = []
    time_series_names = []
    for data_set in data_sets:
        for item in data_set.items:
            if item.type is 'TimeSeries':
                time_series_items.append(item)
                time_series_names.append(item.name)

    return json.dumps({'time_series_names': time_series_names})


@app.route('/api/get_channel_data', methods=['GET'])
def datasets():
    # print(request.method)
    # print(request.headers)
    name = request.headers['Name']
    channel = request.headers['Channel']
    # print(name)
    global bf
    global time_series_items
    data = []
    channel_array = []
    for item in time_series_items:
        print(item.name)
        if item.name == name:
            data = item.get_data(length='1s')
    for key in data:
        channel_array = data[key]
        break
    return json.dumps({'data': str(channel_array.tolist())})

@app.route('/api/user/', methods=['GET'])
def user():
    print(request.method)
    print(request.headers)
    print('its a get!')

    r = requests.get("https://api.blackfynn.io/datasets", headers={'X-SESSION-ID': session_id})

    print(r.status_code, r.reason)
    print(r.content)
    content = r.content
    response = json.loads(content.decode("utf-8"))
    return json.dumps(response)


@app.route('/api/get-dataset/<string:dataset_id>', methods=['GET'])
def datasetId(dataset_id):
    print(dataset_id)
    print(request.method)
    print(request.headers)
    print('its a get!')

    r = requests.get("https://api.blackfynn.io/datasets/"+dataset_id, headers={'X-SESSION-ID': session_id})

    print(r.status_code, r.reason)
    print(r.content)
    content = r.content
    response = json.loads(content.decode("utf-8"))
    return json.dumps(response)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = search_book(books, book_id)
    if book is None:
        abort(404)

    content = json.dumps(book)
    return content, 200, {'Content-Type': JSON_MIME_TYPE}


@app.errorhandler(404)
def not_found(e):
    return '', 404
