from flask import jsonify
from app import app
from middleware import get_github_data

#defines routes and error handling

@app.route('/api/repos/<username>')
def user_repos(username):
    data = get_github_data(username)
    return jsonify(data)

@app.errorhandler(Exception)
def handle_error(e):
    # Log the error for debugging purposes
    app.logger.error(f"An error occurred: {str(e)}")
    
    # Return a JSON response with an appropriate error message and status code
    return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/protected')
def protected_route():
    return jsonify({"message": "Authenticated successfully"}), 200
