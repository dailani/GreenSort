import json
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from util import crop_seperate_objects, analyze_image,getcategory
import concurrent.futures

from util2 import getuser, getadress

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/getItems', methods=['POST'])
def item() -> Response:
    image: str = json.loads(request.data)["image"]
    print(image)
    items: list[str] = crop_seperate_objects(image)

    return jsonify(items)


@app.route('/getMaterial', methods=['POST'])
def material() -> Response:
    images: list[str] = json.loads(request.data)["images"]
    for item in images:
        print(item)

    results = [None] * len(images)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(analyze_image, item): item for item in images}

        i: int
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result: dict[str, list[str]] = future.result()
            results[i] = result

    return jsonify(results)


@app.route('/getCategory', methods=['POST'])
def getCategory() -> Response:
    material: list[str] = json.loads(request.data)[0]["material"]
    things: list[str] = json.loads(request.data)[0]["things"]
    r = getcategory(material,things)

    return jsonify(r)

@app.route('/users/<name>/password/<pw>', methods=['GET'])
def getUser(name, pw) -> Response:
    print(name)
    print(pw)
    r = getuser(name, pw)
    return jsonify(r)


@app.route('/method/<category>', methods=['GET'])
def getAdress(category) -> Response:
    print(category)
    r = getadress(category)
    return jsonify(r)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
