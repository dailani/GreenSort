import base64
import json

from PIL import Image

from flask import Flask, request, Response,jsonify

from util import crop_seperate_objects

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/upload', methods=['POST'])
def get_data() -> Response:

    s:str = json.loads(request.data)["image"]
    print(s)
    items:list[bytes] = crop_seperate_objects(s)

    return jsonify(items)

if __name__ == '__main__':
    app.run()
