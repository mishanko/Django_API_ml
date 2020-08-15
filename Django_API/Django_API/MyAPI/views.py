from .models import Sentiment
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.core import serializers
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import SentimentSerializer
import pandas as pd
import re
import joblib
import fasttext.util
import smart_open
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
from MyAPI.templates.forms import SentimentForm


# Create your views here.
class SentimentView(viewsets.ModelViewSet):
    queryset = Sentiment.objects.all() # get request
    serializer_class = SentimentSerializer

# @api_view(["POST"])
def classifier(unit):
    try:
        model_sentiment = fasttext.load_model("/app/MyAPI/research_package/model_review_fasttext_sentiment.bin") # Загружаем модель
        model_rating = fasttext.load_model("/app/MyAPI/research_package/model_review_fasttext.bin")
        # Обрабатываем текста

        text = re.sub('<[^>]*>', '', str(unit))
        emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
        text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')
        porter = PorterStemmer()

        stop = stopwords.words('english')
        text_rating = [w for w in [porter.stem(word) for word in text.split()] if w not in stop]

        str1 = ' '
        text_rating = str1.join(text_rating)

        # Делаем предсказание
        prediction_sentiment = model_sentiment.predict(text)
        prediction_rating = model_rating.predict(text)
        pred_sent = prediction_sentiment[0][0][9:13]
        pred_rat = prediction_rating[0][0][9:13]
        sentiment = 'Positive'
        if pred_sent == '0':
            sentiment = "Negative"
        return(sentiment, pred_rat)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def cxcontact(request):
    if request.method=='POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data['review']
            prediction = classifier(review)
            messages.success(request, 'Your Sentiment is {} and rating is {}'.format(prediction[0], prediction[1]))

    form = SentimentForm()
    return render(request, 'myform/cxform.html', {'form': form})
