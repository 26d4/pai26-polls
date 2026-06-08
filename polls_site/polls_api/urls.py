from django.urls import path
from . import views

urlpatterns = [
	path('polls/', views.PollList.as_view())
]