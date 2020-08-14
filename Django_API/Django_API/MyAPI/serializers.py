from rest_framework import serializers
from .models import Sentiment

class SentimentSerializer(serializers.ModelSerializer): # check
    class Meta:
        model=Sentiment
        fields='__all__' # видеть все поля
