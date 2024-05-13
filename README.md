GitHub Stats Visualizer

GitHub Stats Visualizer is a tool for generating visualizations of GitHub repository statistics, such as code frequency, commit activity, contributors, and stargazer history.

## Overview

This project consists of two main components:

1. **Downloader**: A Python script (`downloader.py`) responsible for fetching data from the GitHub API and caching it locally.
2. **Visualizer**: Another Python script (`visualizer.py`) that uses the downloaded data to generate various visualizations, such as line charts, pie charts, and grid plots.

## Features

- Retrieve statistics about a GitHub repository, including code frequency, commit activity, contributors, issues, and stargazers.
- Generate visualizations of the retrieved data to gain insights into the repository's development history and community engagement.
- Customize the visualizations by specifying parameters such as repository owner, repository name, and visualization type.

## Usage

To use the GitHub Stats Visualizer:

1. Clone this repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`.
   - pip install requests pandas matplotlib
   - pip freeze > requirements.txt
4. Modify the `main.py` file to specify the repository owner and name, as well as the desired visualization type.
5. Run `python main.py` to generate the visualization.
6. View the generated visualization in the output.

## Dependencies

The GitHub Stats Visualizer relies on the following Python libraries:

- `requests`: For making HTTP requests to the GitHub API.
- `pandas`: For data manipulation and analysis.
- `matplotlib`: For generating visualizations such as line charts, pie charts, and grid plots.

## Contribution

Contributions to the GitHub Stats Visualizer project are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

My Stats

[![](https://raw.githubusercontent.com/Khayaeljuniormokoena/Github-Stats-Visualizer-project/master/profile-summary-card-output/moonlight/0-profile-details.svg)](https://github.com/vn7n24fzkq/github-profile-summary-cards)
[![](https://raw.githubusercontent.com/Khayaeljuniormokoena/Github-Stats-Visualizer-project/master/profile-summary-card-output/moonlight/1-repos-per-language.svg)](https://github.com/vn7n24fzkq/github-profile-summary-cards) [![](https://raw.githubusercontent.com/Khayaeljuniormokoena/Github-Stats-Visualizer-project/master/profile-summary-card-output/moonlight/2-most-commit-language.svg)](https://github.com/vn7n24fzkq/github-profile-summary-cards)
[![](https://raw.githubusercontent.com/Khayaeljuniormokoena/Github-Stats-Visualizer-project/master/profile-summary-card-output/moonlight/3-stats.svg)](https://github.com/vn7n24fzkq/github-profile-summary-cards) [![](https://raw.githubusercontent.com/Khayaeljuniormokoena/Github-Stats-Visualizer-project/master/profile-summary-card-output/moonlight/4-productive-time.svg)](https://github.com/vn7n24fzkq/github-profile-summary-cards)
