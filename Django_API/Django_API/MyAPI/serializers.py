from rest_framework import serializers
from .models import Sentiment

class SentimentSerializer(serializers.ModelSerializer): # переводит данные в json формат для передачи через API
    class Meta:
        model=Sentiment
        fields='__all__' # видеть все поля
