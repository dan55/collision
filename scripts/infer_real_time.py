from google.cloud import bigquery

def update_db(status):
  client = bigquery.Client(project=PROJECT_ID)
  client.query(f"UPDATE hawkai.caltran_camera_signals SET supervised_classifier_signal = {status} WHERE camera_name = '5_elkhorn';")
  
PROJECT_ID = 'w266-nlp-course'
THRESH = 0.3 # consider a frame with probability of collision greater than this to be a collision
MAX_FRAMES = 10 # stop processing after this many frames

# reset camera state
update_db('False')

model = 'rounded_graph_org.pb'
with tf.gfile.FastGFile(model, 'rb') as f:
  graph_def = tf.GraphDef()
  graph_def.ParseFromString(f.read())
  _ = tf.import_graph_def(graph_def, name='')
  
with tf.Session() as sess:
  softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
  
  cap = cv2.VideoCapture()
  cap.open('rtmp://wzmedia.dot.ca.gov/D3/5_elkhorn.stream')
  
  i = 0
  while True:
    ret, frame = cap.read() 
    
    if not ret or i == MAX_FRAMES:
      break
    
    i += 1
  
    predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
    if predictions[0][0] > THRESH:
      update_db('True')