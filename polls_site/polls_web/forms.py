from django import forms
# from django.forms import inlineformset_factory
from polls_api.models import PollChoice, PollQuestion


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


class PollChoiceForm(forms.ModelForm):
	class Meta:
		model = PollChoice
		fields = ['choice_text']


# PollChoiceFormSet = inlineformset_factory(PollQuestion, PollChoice, PollChoiceForm, extra=1, can_delete=False)