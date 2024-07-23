from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load your trained model
model = tf.keras.models.load_model('path/to/your/saved/model.h5')

# Assuming class labels are consistent with the training
# If possible, extract class labels directly from the model or a saved variable
class_labels = ['bike', 'cars', 'cats', 'dogs', 'flowers', 'horses', 'human']  # Replace with your actual class labels

def load_and_preprocess_image(img_path, img_size=(224, 224)):
    img = image.load_img(img_path, target_size=img_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

def predict_image_class(model, img_path):
    img_array = load_and_preprocess_image(img_path)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    return predicted_class, predictions

def interpret_prediction(predicted_class, class_labels):
    return class_labels[predicted_class[0]]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['image']
    file_path = 'static/uploads/' + file.filename
    file.save(file_path)
    
    predicted_class, predictions = predict_image_class(model, file_path)
    predicted_label = interpret_prediction(predicted_class, class_labels)
    
    return jsonify({'label': predicted_label})

if __name__ == '__main__':
    app.run(debug=True)
