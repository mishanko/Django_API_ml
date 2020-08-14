from django.db import models

# Create your models here.
class Sentiment(models.Model):
    review = models.CharField(max_length=10000)

    def __str__(self):
        return self.review
