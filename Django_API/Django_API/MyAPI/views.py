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
from MyAPI.templates.forms import SentimentForm


# Create your views here.
class SentimentView(viewsets.ModelViewSet):
    queryset = Sentiment.objects.all() # get request
    serializer_class = SentimentSerializer

# @api_view(["POST"])
def classifier(unit):
    try:
        path_to_artifacts = "../../research_package/"
        model = fasttext.load_model("/Users/mihailmihaylov/Desktop/Data_science/Проекты/Greenatom/review_project/Django_API_ml/Django_API/Django_API/MyAPI/research_package/model_review_fasttext_sentiment.bin") # Загружаем модель

        # Обработываем текста
        text = re.sub('<[^>]*>', '', str(unit))
        emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
        text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')

        # Делаем предсказание
        prediction = model.predict(text)
        pred = prediction[0][0][9:13]
        sentiment = 'Positive'
        if pred == '0':
            sentiment = "Negative"
        return(sentiment)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)

def cxcontact(request):
    if request.method=='POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data['review']
            prediction = classifier(review)
            messages.success(request, 'Your Sentiment is {}'.format(prediction))

    form = SentimentForm()
    return render(request, 'myform/cxform.html', {'form': form})
