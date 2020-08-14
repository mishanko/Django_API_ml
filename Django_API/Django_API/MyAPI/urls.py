from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("MyAPI", views.SentimentView)

urlpatterns = [
    path('', views.cxcontact, name='cxform'),
    # path('form2/', views.cxcontact2, name='cxform2'),
    # path('api/', include(router.urls)),
    # path('status/', views.classifier)
]
