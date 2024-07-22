from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from model import tfidf, X_train_tfidf, content_based_recommendations, recommend_new_recipe

app = Flask(__name__)

@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        recipe_id = data['recipe_id']
        n_recommendations = data.get('n_recommendations', 5)
        recommendations = content_based_recommendations(recipe_id, X_train_tfidf, n_recommendations)
        return jsonify(recommendations.tolist())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommend_new_recipe', methods=['POST'])
def recommend_new_recipe_endpoint():
    try:
        data = request.get_json()
        recipe_ingredients = data['ingredients']
        n_recommendations = data.get('n_recommendations', 5)
        recommendations = recommend_new_recipe(recipe_ingredients, tfidf, X_train_tfidf, n_recommendations)
        return jsonify(recommendations.tolist())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return "Welcome to the Recipe Recommendation API!"


if __name__ == '__main__':
    app.run(debug=True)
