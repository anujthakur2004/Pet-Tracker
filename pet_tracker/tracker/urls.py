from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("summary/", views.summary_view, name="summary"),
    path("api/chat", views.api_chat, name="api_chat"),
]
