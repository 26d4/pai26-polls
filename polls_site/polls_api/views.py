from rest_framework import generics
from .models import PollQuestion
from .serializers import PollQuestionSerializer, PollQuestionWithChoicesSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from django_eventstream import send_event
from django.contrib.auth import logout, login


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def post(self, request):
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			has_credentials = (
				'username' not in serializer.errors
				and 'password' not in serializer.errors
			)
			message = (
				'Invalid username or password.'
				if has_credentials
				else 'Username and password are required.'
			)
			return Response(
				{
					'message': message,
					'login_success': False,
					'errors': serializer.errors,
				},
				status=400,
			)
		user = serializer.validated_data['user']
		login(request, user)
		# Send success message and flag after creating the session.
		data = dict(UserSerializer(user).data)
		data['message'] = 'Login successful.'
		data['login_success'] = True
		return Response(data)


@api_view(['POST'])
def api_logout(request):
	logout(request)
	return Response(status=204)


class PollListView(generics.ListAPIView):
	queryset = PollQuestion.objects.all()
	serializer_class = PollQuestionSerializer


class PollView(generics.RetrieveAPIView):
	queryset = PollQuestion.objects.prefetch_related('choices')
	serializer_class = PollQuestionWithChoicesSerializer


@api_view(['POST'])
def poll_vote_cast(request, id):
	try:
		print(request.data)
		question = get_object_or_404(PollQuestion, pk=id)
		choice  = question.choices.get(pk=request.data['choice']) # type: ignore
	except (KeyError):
		raise ParseError('Bad choice')
	else:
		if question.has_expired():
			raise ParseError('Voting has concluded')

		choice.votes = F('votes') + 1
		choice.save()
		send_event(f'poll-vote-update-{id}', 'message', {'choice': choice.pk, 'votes': choice.votes})
		return Response(status=204)
	

class PollCreateView(generics.CreateAPIView):
	serializer_class = PollQuestionWithChoicesSerializer
	permission_classes = [IsAuthenticated]
