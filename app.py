import tensorflow as tf

from flask import Flask, jsonify, request
app = Flask(__name__)

# some of the code from here: 
# https://blog.slinto.sk/tensorflow-on-heroku-good-idea-3e6904105892

def create_graph():
    MODEL = 'models/bg_subtract_models_retrained_graph_v3.pb'
    
    with tf.gfile.FastGFile(MODEL, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

def run_inference(image_data):
    create_graph()

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        pred = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = pred[0].argsort()[-len(pred[0]):][::-1]

        prob_collision = pred[0][0]
        return {'collision': str(prob_collision), 
                'no_collision': str(1 - prob_collision)}


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/predict', methods=['POST'])
def predict():
#    data = request.data
    create_graph()
    #res = {'class': 'no_collision'}

    image_data = tf.gfile.FastGFile('images/frame.jpg', 'rb').read()
    res = run_inference(image_data)
    return jsonify(res)
