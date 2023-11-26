from chalice import Chalice
from chalice import BadRequestError
from urllib.parse import urlparse, parse_qs
from chalice import NotFoundError
import json

app = Chalice(app_name='helloworld')

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR'
}
sqs_queue_url = "testqueue"

@app.on_sqs_message(queue=sqs_queue_url)
def index(event):
    # Xử lý sự kiện của SQS ở đây
    for record in event:
        bodyjson = json.loads(record.body)
        print(f"Received bodyjson: {bodyjson}")
        messagejson = json.loads(bodyjson['Message'])
        print(f"Received messagejson: {messagejson}")


# @app.route('/')
# def index():
#     return {'hello': 'world'}

@app.route('/cities/{city}')
def state_of_city(city):
    try:
        return {'state': CITIES_TO_STATE[city]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
            city, ', '.join(CITIES_TO_STATE.keys())))

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
@app.route('/userspost', methods=['POST'])
def create_user():
    # This is the JSON body the user sent in their POST request.
    user_as_json = app.current_request.json_body
    # We'll echo the json body back to the user in a 'user' key.
    return {'user': user_as_json}
#
# See the README documentation for more examples.
#

@app.route('/usersform', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def create_user():
    parsed = parse_qs(app.current_request.raw_body.decode())
    return {
        'states': parsed.get('states', [])
    }

@app.route('/myview', methods=['PUT'])
def myview_put():
    pass

OBJECTS = {
    "test1": "value"
}

@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()
