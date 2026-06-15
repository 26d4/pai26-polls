from django.urls import path
from . import views

urlpatterns = [
	path('polls/', views.PollListView.as_view(), name='api-poll-list'),
	path('poll/<int:pk>/', views.PollView.as_view(), name='api-poll'),
	path('poll/<int:id>/vote', views.poll_vote_cast, name='api-poll-vote-cast'),
	path('poll/', views.PollCreateView.as_view(), name='api-poll-create')
]