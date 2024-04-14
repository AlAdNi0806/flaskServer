# from flask import Flask, request, jsonify


# app = Flask(__name__)


# @app.route('/example', methods=['GET', 'POST'])
# def example():
#     if request.method == 'POST':
#         # Handle POST request
#         # For example, you can access form data using request.form
#         name = request.form.get('name')
#         return f"POST request received with name: {name}"
#     else:
#         # Handle GET request
#         return "GET request received"


# @app.route('/process_data', methods=['POST'])
# def process_data():
#     req_data = request.get_json()
#     # Now req_data is a dictionary containing the JSON data sent in the request
#     print(req_data)
#     print(req_data["name"])
#     print("hello")
#     return 'Data processed'


# @app.route("/im_size", methods=["POST"])
# def process_image():
#     file = request.files['image']
#     # Optionally, you can save the image to disk
#     file.save('im-received.jpg')
#     # Or, read the image using a library like PIL (Python Imaging Library)
#     from PIL import Image
#     img = Image.open(file.stream)
#     # Process the image as needed
#     return jsonify({'msg': 'success', 'size': [img.width, img.height]})


# if __name__ == '__name__':
#     app.run(host='0.0.0.0', port=9000, debug=False)

from shiftlab_ocr.doc2text.reader import Reader
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from uuid import uuid4
from PIL import Image
import io
import os
import urllib.request
import matplotlib.pyplot as plt


app = Flask(__name__)

upload_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(upload_dir, exist_ok=True)


def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"


@app.route('/')
def index():
    return 'Hwllfposaidjff '


@app.route('/im_size', methods=['POST'])
def get_image_size():
    if 'image' not in request.files:
        print("apsodifjaspodf")
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400
    if file:
        img = Image.open(io.BytesIO(file.read()))
        return jsonify({'size': [img.width, img.height]})


@app.route('/getText', methods=['POST'])
def getText():
    if 'image' not in request.files:
        print("apsodifjaspodf")
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400
    if file:
        # img = Image.open(io.BytesIO(file.read()))

        # urllib.request.urlretrieve(
        #     'https://raw.githubusercontent.com/konverner/shiftlab_ocr/main/demo_image.png',
        #     'test.png')

        # img = Image.open('test.png')
        # img

        # reader = Reader()
        # result = reader.doc2text(file)

        # print(result[0])
        # return("successfulll extraction")

        # Open the JPG image

        # Assuming 'file' is a PIL Image object
        unique_filename = make_unique(file.name) + ".jpeg"
        # Change the file extension to '.png'

        # png_filename = os.path.splitext(unique_filename)[0] + '.png'
        # png_filename = unique_filename

        # Save the image as a PNG
        file.save(os.path.join(upload_dir, unique_filename))

        print("Successful save")

        # Construct the path to the saved PNG file
        png_file_path = os.path.join(upload_dir, unique_filename)

        # Now, pass the path to the PNG file to the Reader
        reader = Reader()
        result = reader.doc2text(png_file_path)

        print(result[0])

        print("successfulll extraction")

        os.remove(png_file_path)

        return (result[0])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
