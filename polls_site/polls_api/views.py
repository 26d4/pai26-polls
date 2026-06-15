from rest_framework import generics
from .models import PollQuestion
from .serializers import PollQuestionSerializer, PollQuestionWithChoicesSerializer
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError


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
		return Response(status=204)
	

class PollCreateView(generics.CreateAPIView):
	serializer_class = PollQuestionWithChoicesSerializer
