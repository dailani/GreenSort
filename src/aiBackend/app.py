import json
from flask import Flask, request, Response, jsonify
from util import crop_seperate_objects, analyze_image
import concurrent.futures

app = Flask(__name__)


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

    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(analyze_image, item): item for item in images}

        for i ,future in enumerate(concurrent.futures.as_completed(futures)):
            result: dict[str, list[str]] = future.result()
            results[str(i)] = result

    return jsonify(results)


if __name__ == '__main__':
    app.run()
