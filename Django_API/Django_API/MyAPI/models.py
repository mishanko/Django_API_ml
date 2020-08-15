from django.db import models

# Create your models here.
class Sentiment(models.Model):
    review = models.CharField(max_length=10000) # текстовое поле максимальной длинной в 10000 символов

    def __str__(self):
        return self.review
