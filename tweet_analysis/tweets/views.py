from django.shortcuts import render
from django.db.models import Count
from .models import TweetAnalysis


def tweet_list(request):
    tweets = TweetAnalysis.objects.all()
    sentiment_counts = tweets.values('sentiment').annotate(total=Count('sentiment')).order_by('sentiment')
    sentiment_data = {item['sentiment']: item['total'] for item in sentiment_counts}
    return render(request, 'tweets/tweet_list.html', {'tweets': tweets, 'sentiment_data': sentiment_data})
