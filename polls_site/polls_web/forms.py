from django import forms
from polls_api.models import PollChoice, PollQuestion
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction


class PollQuestionForm(forms.ModelForm):
	num_choices = forms.IntegerField(min_value=0, widget=forms.HiddenInput())

	class Meta:
		model = PollQuestion
		fields = ['question_text', 'exp_date']
		widgets = {
			'exp_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
		}

	def __init__(self, *args, **kwargs):
		num_choices = kwargs.pop('num_choices')
		super().__init__(*args, **kwargs)
		self.initial = {'num_choices': num_choices}
		for i in range(num_choices):
			self.fields[f'choice_{i}'] = PollChoice._meta.get_field('choice_text').formfield(label=f'Choice #{i+1}')

	def save(self, commit=True, owner=None):
		with transaction.atomic():
			question = super().save(commit=False)
			question.owner = owner
			if commit:
				question.save()
			choices = [PollChoice(choice_text=v, question=question) for k, v in self.cleaned_data.items() if k.startswith('choice')]
			if commit:
				PollChoice.objects.bulk_create(choices)
		return question, choices


class PollChoiceForm(forms.ModelForm):
	class Meta:
		model = PollChoice
		fields = ['choice_text']


class RegisterForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ['username']