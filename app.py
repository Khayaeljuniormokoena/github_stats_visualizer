from flask import Flask
from config import load_config
from middleware import setup_cache
from routes import *
from authlib.integrations.flask_client import OAuth

#initializes the Flask application and imports and runs the routes

app = Flask(__name__)
oauth = OAuth(app)

github = oauth.register(
    'github',
    client_id='Ov23liQGzGkwtJUUuEFO',
    client_secret='b092bada213ea91186f6a16e035a2eee8f8ec3af',
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'repo,user'},
)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route('/github/authorize')
def authorize():
    token = github.authorize_access_token()
    resp = github.get('user')
    user_info = resp.json()
    # Process user_info and/or store the token in a secure manner
    return 'You are logged in as: ' + user_info['name']

@app.route('/repo-stats/<username>/<repo>')
def repo_stats(username, repo):
    github = OAuth.create_client('github')  # If session already created
    repo_data = github.get(f'repos/{username}/{repo}').json()
    return jsonify(repo_data)

# Load configurations from config.py
load_config(app)

if __name__ == '__main__':
    app.run(debug=True)
