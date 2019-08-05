import os
from pathlib import Path

"""
Generate predictions from the frames in the `frames` directory.

These can be generated from a video with:

import cv2 
vidcap = cv2.VideoCapture('crash.mp4')

while True:
    success, image = vidcap.read()
    if not success:
      break

    cv2.imwrite("frames/frame%s.jpg" % f'{count:04}', image) # save frame as JPEG file in a sortable order
"""
from google.cloud import bigquery

def update_db(status):
  client = bigquery.Client(project=PROJECT_ID)
  client.query(f"UPDATE hawkai.caltran_camera_signals SET supervised_classifier_signal = {status} WHERE camera_name = '5_elkhorn';")

# reset camera state
update_db('False')

model = 'rounded_graph_org.pb'
with tf.gfile.FastGFile(model, 'rb') as f:
  graph_def = tf.GraphDef()
  graph_def.ParseFromString(f.read())
  _ = tf.import_graph_def(graph_def, name='')
  
with tf.Session() as sess:
  softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
  
  i = 0
  for frame in sorted(os.listdir('frames')):
    frame = 'frames/' + frame  
    image_data = tf.gfile.FastGFile(frame, 'rb').read()
    predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})   # analyse the image

    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
    THRESH = 0.3
    if predictions[0][0] > THRESH:
      update_db('True')