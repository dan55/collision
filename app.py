import numpy as np
import tensorflow as tf

from flask import (
        Flask,
        jsonify,
        render_template,
        request)

app = Flask(__name__)
global graph
# some of the code from here: 
# https://blog.slinto.sk/tensorflow-on-heroku-good-idea-3e6904105892

def create_graph():
    MODEL = 'models/bg_subtract_models_retrained_graph_v3.pb'
    
    with tf.gfile.FastGFile(MODEL, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        res = tf.import_graph_def(graph_def, name='')
	return res

def run_inference(image_data):

    with tf.Session(graph=graph) as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        pred = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = pred[0].argsort()[-len(pred[0]):][::-1]

        prob_collision = pred[0][0]
    return {'collision': str(prob_collision), 
                'no_collision': str(1 - prob_collision)}

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/abt')
def about():
    return render_template('about.html')

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/predict', methods=['POST'])
def predict():
    res = run_inference(request.data)
    return jsonify(res)

if __name__ == '__main__':
    graph = create_graph()
    app.run()
