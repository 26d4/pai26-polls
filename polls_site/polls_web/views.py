from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic
import django.contrib.auth.views as auth_views
from django.utils.cache import patch_vary_headers
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db.models import F
from django_eventstream import send_event
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import engines
from django.contrib.auth import get_user_model

from polls_api.models import PollQuestion
from .forms import PollQuestionForm, RegisterForm


class RegisterView(generic.CreateView):
	model = get_user_model()
	form_class = RegisterForm
	template_name = 'polls_web/register.html'

	def get_success_url(self) -> str:
		return reverse('polls_web:index')


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
		send_event(f'hx-poll-vote-update-{pk}', f'choice-{choice.pk}', f'{choice.votes}', json_encode=False)
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
	engine = engines['django']
	template = engine.from_string(
'''
<tbody hx-swap-oob="beforeend:table tbody">
	<tr>
		<th>{{ form.choice_%i.label_tag }}</th><td>{{ form.choice_%i }}</td>
	</tr>
</tbody>

<input id=id_num_choices name=num_choices value=%i type=hidden hx-swap-oob=outerHTML>
	
<button hx-get="/poll-form-choice-row/%i" hx-target="#replace-me" hx-swap="innerHTML">Add choice</button>
''' % (number, number, number+1, number+1))

	form = PollQuestionForm(num_choices=number+1)

	html = template.render({'form': form})
	return HttpResponse(html)


@login_required
def poll_create(request):
	if request.method == "POST":
		data = request.POST

		form = PollQuestionForm(data, num_choices=int(data['num_choices']))

		if form.is_valid():
			question, choices = form.save(owner=request.user, commit=True)
			return redirect('polls_web:detail', pk=question.pk)
		else:
			return render(request, 'polls_web/new.html', {'form': form})
	else:
		form = PollQuestionForm(None, num_choices=1)
	return render(request, 'polls_web/new.html', {'form': form})
