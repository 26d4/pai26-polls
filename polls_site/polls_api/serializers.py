from rest_framework import serializers
from .models import PollQuestion, PollChoice
from django.contrib.auth import get_user_model, authenticate
from django.db.transaction import atomic

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(
		write_only=True,
		style={'input_type': 'password'},
	)

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

	def create(self, validated_data):
		return User.objects.create_user(
			**validated_data
		)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=attrs['password'],
        )
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = fields


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

		with atomic():
			question = PollQuestion.objects.create(**validated_data)
			for choice in choices:
				PollChoice.objects.create(question=question, **choice)
				
		return question

	class Meta(PollQuestionSerializer.Meta):
		pass