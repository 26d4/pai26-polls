from rest_framework import serializers
from .models import PollQuestion, PollChoice


class PollQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = PollQuestion
		fields = '__all__'
		read_only_fields = [f. name for f in PollQuestion._meta.get_fields()]


class PollChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = PollChoice
		fields = '__all__'
		read_only_fields = ['id', 'question', 'choice_text']


class PollQuestionWithChoicesSerializer(PollQuestionSerializer):
	choices = PollChoiceSerializer(many=True)
	class Meta(PollQuestionSerializer.Meta):
		pass