from flask import Flask, render_template, send_file
from visualizer import Visualizer
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Set up the visualizer with the owner and repo name
owner = "octocat"
repo = "Hello-World"
visualizer = Visualizer(owner, repo)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_charts')
def generate_charts():
    visualizer.lines_over_time()
    visualizer.commits_by_author()
    visualizer.stargazer_history()
    visualizer.commit_activity()
    return render_template('charts.html')

@app.route('/static/images/&lt;filename&gt;')
def serve_image(filename):
    return send_file(os.path.join('static/images', filename))

if __name__ == "__main__":
    app.run(debug=True)
