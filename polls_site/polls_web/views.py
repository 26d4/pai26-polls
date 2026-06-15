from django.shortcuts import redirect
from django.views import generic

from polls_api.models import PollQuestion


class IndexView(generic.ListView):
	template_name = "polls_web/index.html"
	context_object_name = "latest_questions"

	def get_queryset(self):
		return PollQuestion.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
	model = PollQuestion
	template_name = "polls_web/detail.html"
	context_object_name = 'question'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.has_expired(): # type: ignore
			return redirect('polls_web:results', pk=self.object.pk)
		return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
	model = PollQuestion
	template_name = 'polls_web/results.html'
	context_object_name = 'question'


class CreateView(generic.CreateView):
	pass