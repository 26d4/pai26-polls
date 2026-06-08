from rest_framework import generics
from .models import PollQuestion
from .serializers import PollQuestionWithChoicesSerializer

class PollList(generics.ListAPIView):
	queryset = PollQuestion.objects.all()
	serializer_class = PollQuestionWithChoicesSerializer
