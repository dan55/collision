import tensorflow as tf

from flask import Flask, jsonify, request
app = Flask(__name__)

# some of the code from here: 
# https://blog.slinto.sk/tensorflow-on-heroku-good-idea-3e6904105892

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.data
    print(data)
    print(tf.version)
    return "hello"
    # return jsonify(data)