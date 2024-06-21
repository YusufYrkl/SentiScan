# SentiScan Tweet Analysis

SentiScan is a web application that processes and analyzes tweets for sentiment. It uses a pre-trained sentiment analysis model to classify tweets as positive, neutral, or negative. The application allows users to view, filter, comment, and export analyzed tweets.
Features

- Load and analyze tweets from a CSV file
- Filter tweets by sentiment, confidence, and keyword
- Add and delete comments on tweets
- Export filtered tweets to a CSV file
- View sentiment analysis graphs

### Setup Guide

Follow these steps to set up and run the SentiScan project locally.
#### Prerequisites

- Python 3.x
- pip (Python package installer)
- SQLite (included with Python)
- Git
- Virtual Environment with requirements installed

#### Installation

#### Setup a virtual python Environment
- Simplest way is to use PyCharm and create a new Project

#### Clone the repository
```
git clone https://github.com/yourusername/sentiscan.git
```

#### install the Requirements
```
pip install -r requirements.txt
```

#### Run the development server
```
python manage.py runserver
```

Open your browser and navigate to http://127.0.0.1:8000/

#### Main Script for Sentiment Analysis

The main.py script is used to load tweets from a CSV file, preprocess them, analyze their sentiment, and store the results in the SQLite database. To run this script:
- python main.py

### Project Structure

    tweet_analysis/: Main Django application directory
        tweets/: Contains models, views, and templates for tweet analysis
        migrations/: Database migrations
    templates/tweets: HTML templates for the web application
    main.py: Script for loading and analyzing tweets
    requirements.txt: List of Python dependencies

#### Adding More Tweets
To add more tweets, update the main.py [row 32] script to process the desired range of tweets and run it again.


This project is licensed under the MIT License.
