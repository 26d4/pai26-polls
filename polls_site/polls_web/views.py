from django.shortcuts import redirect, render
from django.views import generic
import django.contrib.auth.views as auth_views
from django.utils.cache import patch_vary_headers
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db.models import F
from django_eventstream import send_event
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from polls_api.models import PollQuestion, PollChoice


class LoginView(auth_views.LoginView):
	template_name = 'polls_web/login.html'
	redirect_authenticated_user = True


class IndexView(generic.ListView):
	template_name = "polls_web/index.html"
	context_object_name = "latest_questions"

	def get_queryset(self):
		return PollQuestion.objects.order_by("-pub_date")[:5]
	
	def dispatch(self, *args, **kwargs):
		response = super().dispatch(*args, **kwargs)
		patch_vary_headers(response, ['HX-Boosted']) # type: ignore
		return response

	def get_template_names(self):
		if self.request.htmx.boosted: # type: ignore
			return [self.template_name + "#content"]
		return super().get_template_names()


class DetailView(generic.DetailView):
	model = PollQuestion
	template_name = "polls_web/detail.html"
	context_object_name = 'question'

	def dispatch(self, *args, **kwargs):
		response = super().dispatch(*args, **kwargs)
		patch_vary_headers(response, ['HX-Boosted']) # type: ignore
		return response

	def get_template_names(self):
		if self.request.htmx.boosted: # type: ignore
			return [self.template_name + "#content"]
		return super().get_template_names()
	

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.has_expired(): # type: ignore
			return redirect('polls_web:results', pk=self.object.pk)
		return super().get(request, *args, **kwargs)


@require_POST
def vote_cast(request, pk):
	try:
		question = get_object_or_404(PollQuestion, pk=pk)
		choice  = question.choices.get(pk=request.POST['choice']) # type: ignore
	except (KeyError):
		redirect('polls_web:results', pk=pk)
	else:
		if question.has_expired():
			return redirect('polls_web:results', pk=pk)

		choice.votes = F('votes') + 1
		choice.save()
		send_event(f'poll-vote-update-{pk}', 'message', {'choice': choice.pk, 'votes': choice.votes})
		return redirect('polls_web:results', pk=pk)


class ResultsView(generic.DetailView):
	model = PollQuestion
	template_name = 'polls_web/results.html'
	context_object_name = 'question'

	def dispatch(self, *args, **kwargs):
		response = super().dispatch(*args, **kwargs)
		patch_vary_headers(response, ['HX-Boosted']) # type: ignore
		return response

	def get_template_names(self):
		if self.request.htmx.boosted: # type: ignore
			return [self.template_name + "#content"]
		return super().get_template_names()


def choice_row(request, number):
	return HttpResponse(f'''
	<input type="text" name="choice-{number}"><br>
	<div id="replace-me">
	<button hx-get="/poll-form-choice-row/{number+1}" hx-target="#replace-me" hx-swap="outerHTML">Add choice</button>
	</div>''')


@login_required
def poll_create(request):
	if request.method == "POST":
		data = request.POST

		question = PollQuestion()
		choices = []

		for k, v in data.items():
			if k == 'question_text':
				question.question_text = v
			elif k == 'exp_date':
				question.exp_date = v
			elif k.startswith('choice'):
				choices.append(PollChoice(choice_text=v, question=question))
			
		
		question.save()
		PollChoice.objects.bulk_create(choices)
		return redirect('polls_web:index')
	else:
		return render(request, 'polls_web/new.html')