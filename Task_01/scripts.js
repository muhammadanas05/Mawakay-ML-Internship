document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('recipe-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const recipeId = document.getElementById('recipe-id').value;
        const numRecommendations = document.getElementById('num-recommendations').value;

        fetch('/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                recipe_id: parseInt(recipeId),
                n_recommendations: parseInt(numRecommendations)
            })
        })
        .then(response => response.json())
        .then(data => {
            const recommendationsList = document.getElementById('recommendations-list');
            recommendationsList.innerHTML = '<h3>Recommendations:</h3>';
            data.forEach(id => {
                recommendationsList.innerHTML += `<p>Recipe ID: ${id}</p>`;
            });
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('new-recipe-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const ingredients = document.getElementById('ingredients').value;
        const numRecommendationsNew = document.getElementById('num-recommendations-new').value;

        fetch('/recommend_new_recipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ingredients: ingredients,
                n_recommendations: parseInt(numRecommendationsNew)
            })
        })
        .then(response => response.json())
        .then(data => {
            const recommendationsList = document.getElementById('new-recipe-recommendations-list');
            recommendationsList.innerHTML = '<h3>Recommendations:</h3>';
            data.forEach(id => {
                recommendationsList.innerHTML += `<p>Recipe ID: ${id}</p>`;
            });
        })
        .catch(error => console.error('Error:', error));
    });
});
