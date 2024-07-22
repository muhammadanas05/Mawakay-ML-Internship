import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the datasets
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# Preprocess data
train.fillna('', inplace=True)
test.fillna('', inplace=True)
train['all_ingredients'] = train['ingredients'].apply(lambda x: ' '.join(x.split(',')))
test['all_ingredients'] = test['ingredients'].apply(lambda x: ' '.join(x.split(',')))

# Convert ingredients into TF-IDF features
tfidf = TfidfVectorizer(stop_words='english')
X_train_tfidf = tfidf.fit_transform(train['all_ingredients'])
X_test_tfidf = tfidf.transform(test['all_ingredients'])

def content_based_recommendations(recipe_id, X_tfidf, n_recommendations=5):
    cosine_similarities = cosine_similarity(X_tfidf[recipe_id], X_tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-n_recommendations-1:-1]
    return related_docs_indices

def recommend_new_recipe(recipe_ingredients, tfidf, X_tfidf, n_recommendations=5):
    new_recipe_tfidf = tfidf.transform([recipe_ingredients])
    cosine_similarities = cosine_similarity(new_recipe_tfidf, X_tfidf).flatten()
    related_docs_indices = cosine_similarities.argsort()[:-n_recommendations-1:-1]
    return related_docs_indices
