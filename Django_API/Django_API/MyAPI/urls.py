from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("MyAPI", views.SentimentView)

urlpatterns = [
    path('', views.cxcontact, name='cxform'),
]
