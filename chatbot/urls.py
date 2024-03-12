# urls.py

from django.urls import path
from .views import ChatBotAPIView

urlpatterns = [
    path('chatbot/', ChatBotAPIView.as_view(), name='chatbot'),
    # Autres URLs de votre application...
]
