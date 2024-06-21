import csv
from django.http import HttpResponse
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from .models import TweetAnalysis
from django.db.models import Count
import subprocess
import os


def get_sentiment_data():
    tweets = TweetAnalysis.objects.all()
    sentiment_counts = tweets.values('sentiment').annotate(total=Count('sentiment')).order_by('sentiment')
    sentiment_data = {item['sentiment']: item['total'] for item in sentiment_counts}
    return sentiment_data


def tweet_list(request):
    sentiment = request.GET.get('sentiment')
    min_confidence = request.GET.get('min_confidence')
    keyword = request.GET.get('keyword')

    tweets = TweetAnalysis.objects.all()

    if sentiment:
        tweets = tweets.filter(sentiment=sentiment)

    if min_confidence:
        try:
            min_confidence = float(min_confidence)
            tweets = tweets.filter(confidence__gte=min_confidence)
        except ValueError:
            pass  # Ignore invalid input

    if keyword:
        tweets = tweets.filter(tweet__icontains=keyword)

    sentiment_data = get_sentiment_data()
    total_tweets = TweetAnalysis.objects.count()

    if request.method == 'POST' and 'start' in request.POST and 'end' in request.POST:
        start = int(request.POST.get('start', 0))
        end = int(request.POST.get('end', 50))
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(project_root, 'main.py')
        try:
            result = subprocess.run(['python', script_path, str(start), str(end)], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
        except Exception as e:
            print(e)
        return redirect('tweet_list')

    return render(request, 'tweets/tweet_list.html',
                  {'tweets': tweets, 'sentiment_data': sentiment_data, 'total_tweets': total_tweets})


def export_tweets(request):
    sentiment = request.GET.get('sentiment')
    min_confidence = request.GET.get('min_confidence')
    keyword = request.GET.get('keyword')

    tweets = TweetAnalysis.objects.all()

    if sentiment:
        tweets = tweets.filter(sentiment=sentiment)

    if min_confidence:
        try:
            min_confidence = float(min_confidence)
            tweets = tweets.filter(confidence__gte=min_confidence)
        except ValueError:
            pass  # Ignore invalid input

    if keyword:
        tweets = tweets.filter(tweet__icontains=keyword)

    # Erstelle den Zeitstempel für den Dateinamen
    timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"tweets_{timestamp}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['id', 'tweet', 'sentiment', 'confidence'])

    for tweet in tweets:
        writer.writerow([tweet.id, tweet.tweet, tweet.sentiment, tweet.confidence])

    return response


def graphs(request):
    sentiment_data = get_sentiment_data()
    return render(request, 'tweets/graphs.html', {'sentiment_data': sentiment_data})