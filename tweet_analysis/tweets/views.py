import csv
from django.http import HttpResponse
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from .models import TweetAnalysis
from django.db.models import Count
import subprocess
import os
from django.conf import settings

def get_sentiment_data():
    # Retrieve all TweetAnalysis objects
    tweets = TweetAnalysis.objects.all()

    # Aggregate sentiment counts, ordering by sentiment type
    sentiment_counts = tweets.values('sentiment').annotate(total=Count('sentiment')).order_by('sentiment')

    # Convert the aggregation result into a dictionary with sentiment as keys and counts as values
    sentiment_data = {item['sentiment']: item['total'] for item in sentiment_counts}
    return sentiment_data

def tweet_list(request):
    # Get filter parameters from the request
    sentiment = request.GET.get('sentiment')
    min_confidence = request.GET.get('min_confidence')
    keyword = request.GET.get('keyword')

    # Retrieve all TweetAnalysis objects
    tweets = TweetAnalysis.objects.all()

    # Filter by sentiment if provided
    if sentiment:
        tweets = tweets.filter(sentiment=sentiment)

    # Filter by minimum confidence if provided and valid
    if min_confidence:
        try:
            min_confidence = float(min_confidence)
            tweets = tweets.filter(confidence__gte=min_confidence)
        except ValueError:
            pass  # Ignore invalid input

    # Filter by keyword if provided
    if keyword:
        tweets = tweets.filter(tweet__icontains=keyword)

    # Get sentiment data and total tweet count
    sentiment_data = get_sentiment_data()
    total_tweets = TweetAnalysis.objects.count()

    # Check if the request method is POST and required parameters are provided
    if request.method == 'POST' and 'start' in request.POST and 'end' in request.POST:
        start = int(request.POST.get('start', 0))
        end = int(request.POST.get('end', 50))

        # Get the project root directory and the path to the main.py script
        script_path = os.path.join(settings.BASE_DIR, '../main.py')
        python_interpreter = os.path.join(settings.BASE_DIR, '../.venv/Scripts/python.exe')

        # Run the main.py script with start and end parameters
        try:
            result = subprocess.run([python_interpreter, script_path, str(start), str(end)], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        except Exception as e:
            print(e)

        # Redirect to the tweet_list view
        return redirect('tweet_list')

    # Render the tweet_list template with the filtered tweets and additional data
    return render(request, 'tweets/tweet_list.html',
                  {'tweets': tweets, 'sentiment_data': sentiment_data, 'total_tweets': total_tweets})

def export_tweets(request):
    # Get filter parameters from the request
    sentiment = request.GET.get('sentiment')
    min_confidence = request.GET.get('min_confidence')
    keyword = request.GET.get('keyword')

    # Retrieve all TweetAnalysis objects
    tweets = TweetAnalysis.objects.all()

    # Filter by sentiment if provided
    if sentiment:
        tweets = tweets.filter(sentiment=sentiment)

    # Filter by minimum confidence if provided and valid
    if min_confidence:
        try:
            min_confidence = float(min_confidence)
            tweets = tweets.filter(confidence__gte=min_confidence)
        except ValueError:
            pass  # Ignore invalid input

    # Filter by keyword if provided
    if keyword:
        tweets = tweets.filter(tweet__icontains=keyword)

    # Generate a timestamp for the filename
    timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"tweets_{timestamp}.csv"

    # Create an HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Write CSV header
    writer = csv.writer(response)
    writer.writerow(['id', 'tweet', 'sentiment', 'confidence'])

    # Write tweet data to CSV
    for tweet in tweets:
        writer.writerow([tweet.id, tweet.tweet, tweet.sentiment, tweet.confidence])

    return response

def graphs(request):
    # Get sentiment data
    sentiment_data = get_sentiment_data()

    # Render the graphs template with sentiment data
    return render(request, 'tweets/graphs.html', {'sentiment_data': sentiment_data})
