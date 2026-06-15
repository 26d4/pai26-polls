from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from django_eventstream.viewsets import configure_events_view_set

router = SimpleRouter(use_regex_path=True)
router.register(
	'events',
	configure_events_view_set(),
	'events'
)

app_name = 'polls_api'
urlpatterns = [
	path('polls/', views.PollListView.as_view(), name='api-poll-list'),
	path('poll/<int:pk>/', views.PollView.as_view(), name='api-poll'),
	path('poll/<int:id>/vote', views.poll_vote_cast, name='api-poll-vote-cast'),
	path('poll/', views.PollCreateView.as_view(), name='api-poll-create'),
	path('', include(router.urls)),
	path('login/', views.LoginView.as_view(), name='api-login'),
	path('logout/', views.api_logout, name='api-logout'),
	path('current-user/', views.MeView.as_view(), name='api-current-user')
]