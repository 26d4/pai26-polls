from rest_framework import serializers
from .models import PollQuestion, PollChoice


class PollQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = PollQuestion
		fields = '__all__'


class PollChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = PollChoice
		fields = '__all__'


class PollQuestionWithChoicesSerializer(PollQuestionSerializer):
	choices = PollChoiceSerializer(many=True)
	class Meta(PollQuestionSerializer.Meta):
		pass