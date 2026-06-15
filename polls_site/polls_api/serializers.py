from rest_framework import serializers
from .models import PollQuestion, PollChoice


class PollQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = PollQuestion
		fields = '__all__'
		read_only_fields = ['id']


class PollChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = PollChoice
		fields = '__all__'
		read_only_fields = ['id', 'question']


class PollQuestionWithChoicesSerializer(PollQuestionSerializer):
	choices = PollChoiceSerializer(many=True)

	def create(self, validated_data):
		choices = validated_data.pop('choices')

		question = PollQuestion.objects.create(**validated_data)
		for choice in choices:
			PollChoice.objects.create(question=question, **choice)
		return question

	class Meta(PollQuestionSerializer.Meta):
		pass