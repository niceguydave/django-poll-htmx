import urllib

from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import SearchForm
from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def search(request):
    form = SearchForm(request.GET or None)

    search_text = " "
    errors = None
    results = []

    if form.is_valid():
        search_text = form.cleaned_data["search_text"]
        search_text = urllib.parse.unquote(search_text)
        search_text = search_text.strip()

        parts = search_text.split()

        q = Q(question_text__icontains=parts[0])
        for part in parts[1:]:
            q |= Q(question_text__icontains=part)

        results = Question.objects.filter(q)
    else:
        errors = form.errors.get("search_text", None)

    data = {
        "search_text": search_text,
        "polls": results,
        "errors": errors,
    }

    if request.htmx:
        return render(request, "polls/partials/search_results.html", data)

    return render(request, "polls/search.html", data)
