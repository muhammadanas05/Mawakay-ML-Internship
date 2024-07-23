# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import joblib

# app = Flask(__name__)
# CORS(app)  # Enable CORS

# # Load the trained model, scaler, and encoder
# model = joblib.load('random_forest_model.pkl')
# scaler = joblib.load('scaler.pkl')
# encoder = joblib.load('encoder.pkl')

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json(force=True)
    
#     # Prepare the input data
#     input_data = [
#         data['Age'],
#         data['Billing Amount'],
#         data['Room Number'],
#         data['Gender'],
#         data['Blood Type'],
#         data['Admission Type'],
#         data['Medication'],
#         data['Test Results']
#     ]
    
#     # Scale and encode input data if necessary
#     input_data = scaler.transform([input_data])  # Example scaling step
#     input_data = encoder.transform(input_data)    # Example encoding step
    
#     prediction = model.predict(input_data)
    
#     return jsonify({'Medical Condition': prediction[0]})

# if __name__ == '__main__':
#     app.run(debug=True)







from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the trained model, scaler, and encoder
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')
encoder = joblib.load('encoder.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    # Prepare the input data
    features = {
        'Age': data.get('Age'),
        'Billing Amount': data.get('Billing Amount'),
        'Room Number': data.get('Room Number'),
        'Age*Billing': data.get('Age') * data.get('Billing Amount'),
        'Gender': data.get('Gender'),
        'Blood Type': data.get('Blood Type'),
        'Admission Type': data.get('Admission Type'),
        'Medication': data.get('Medication'),
        'Test Results': data.get('Test Results')
    }

    # Create a DataFrame
    df = pd.DataFrame([features])
    
    # Encode categorical variables
    categorical_features = ['Gender', 'Blood Type', 'Admission Type', 'Medication', 'Test Results']
    encoded_features = encoder.transform(df[categorical_features])
    
    # Normalize numerical features
    numerical_features = ['Age', 'Billing Amount', 'Room Number', 'Age*Billing']
    scaled_features = scaler.transform(df[numerical_features])
    
    # Concatenate features
    encoded_features_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features))
    scaled_features_df = pd.DataFrame(scaled_features, columns=numerical_features)
    X = pd.concat([scaled_features_df, encoded_features_df], axis=1)

    # Make prediction
    prediction = model.predict(X)[0]

    return jsonify({'Medical Condition': prediction})

if __name__ == '__main__':
    app.run(debug=True)
