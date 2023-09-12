from django.urls import path,include
from .views import ChatView
urlpatterns = [
    path('chat/start/<str:target>', ChatView.as_view(), name="chat"),
]
