import os
from flask import Flask, render_template, request
from flask import send_from_directory
import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

sess = tf.Session()
graph = tf.get_default_graph()

keras.backend.set_session(sess)

model = keras.models.load_model(STATIC_FOLDER + '/' + 'mnist_model.h5')




# call model to predict an image
def model_predict(full_path):
    global sess
    global graph

    im_array = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(im_array, (28, 28))
    new_array = new_array/255.0
    new_array = new_array.reshape(-1,28,28)

    print(new_array.shape, type(new_array))

    with graph.as_default():
        keras.backend.set_session(sess)
        predicted = model.predict(new_array)
        return predicted


# home page
@app.route('/')
def home():
   return render_template('index.html')


# procesing uploaded file and predict it
@app.route('/upload', methods=['POST','GET'])
def upload_file():

    if request.method == 'GET':
        return render_template('index.html')
    else:
        file = request.files['image']
        full_name = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(full_name)

        indices = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4:'Four', 5:'Five', 6:'Six', 7:'Seven', 8:'Eight', 9:'Nine'}
        result = model_predict(full_name)

        predicted_class = np.asscalar(np.argmax(result, axis=1))
        label = indices[predicted_class]

    return render_template('predict.html', image_file_name = file.filename, label = label)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(port= 5002, debug=False,threaded=False)
