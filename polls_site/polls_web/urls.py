from django.urls import path
from . import views
import django.contrib.auth.views as auth_views

app_name = 'polls_web'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('poll/<int:pk>', views.DetailView.as_view(), name='detail'),
	path('poll/<int:pk>/results', views.ResultsView.as_view(), name='results'),
	path('login', views.LoginView.as_view(), name='login'),
	path('logout', auth_views.LogoutView.as_view(), name='logout')
]