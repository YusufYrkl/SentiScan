from django.db import models

class TweetAnalysis(models.Model):
    tweet = models.TextField(unique=True)
    sentiment = models.CharField(max_length=10)
    confidence = models.FloatField()

    class Meta:
        db_table = 'tweet_analysis'

    def __str__(self):
        return self.tweet