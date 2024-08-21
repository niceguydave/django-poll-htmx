import datetime

from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice
from .views import search as search_view


def create_question(question_text, days=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class HTMXQuestionSearchViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        create_question(question_text="This is a test question")
        create_question(question_text="Another question about cats")

    def test_htmx_request_uses_partial_template(self):
        url = reverse("polls:search")
        request = self.factory.get(url, {"search_text": "test"})
        request.htmx = True  # Simulate an HTMX request

        with self.assertTemplateUsed("polls/partials/search_results.html"):
            response = search_view(request)

        self.assertEqual(response.status_code, 200)

    def test_non_htmx_request_uses_full_template(self):
        url = reverse("polls:search")
        request = self.factory.get(url, {"search_text": "test"})
        request.htmx = False  # Simulate a non-HTMX request

        with self.assertTemplateUsed("polls/search.html"):
            response = search_view(request)

        self.assertEqual(response.status_code, 200)

    def test_htmx_request_contains_partial_content(self):
        url = reverse("polls:search")
        request = self.factory.get(url, {"search_text": "test"})
        request.htmx = True  # Simulate an HTMX request

        response = search_view(request)

        self.assertContains(response, "This is a test question")
        self.assertNotContains(response, "Another question about cats")

    def test_non_htmx_request_contains_full_content(self):
        url = reverse("polls:search")
        request = self.factory.get(url, {"search_text": "test"})
        request.htmx = False  # Simulate a non-HTMX request

        response = search_view(request)

        self.assertContains(response, "This is a test question")
        self.assertNotContains(response, "Another question about cats")


class QuestionSearchViewTests(TestCase):

    def setUp(self):
        create_question(question_text="This is a test question")
        create_question(question_text="Another question about cats")

    def test_valid_search(self):
        url = reverse("polls:search")
        response = self.client.get(url, {"search_text": "test question"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<p class="error">')
        self.assertContains(response, "This is a test question")
        self.assertContains(response, "Another question about cats")

    def test_search_with_blocked_word(self):
        url = reverse("polls:search")
        response = self.client.get(url, {"search_text": "🫤"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p class="error">')
        self.assertNotContains(response, "This is a test question")
        self.assertNotContains(response, "Another question about cats")


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

    def test_pagination(self):
        # Create more questions to test pagination
        for i in range(4):
            create_question(question_text=f"Question {i}")

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(len(response.context["question_list"]), 2)
        self.assertTrue(response.context["is_paginated"])

    def test_invalid_page_integer(self):
        response = self.client.get(reverse("polls:index") + "?page=999")
        self.assertEqual(response.status_code, 404)

    def test_invalid_page_number_type(self):
        response = self.client.get(reverse("polls:index") + "?page=obviouslynotanumber")
        self.assertEqual(response.status_code, 404)


class QuestionModelTests(TestCase):
    def test_model_str(self):
        question = create_question(question_text="Good question")
        assert question.__str__() == "Good question"

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class ChoiceModelTests(TestCase):
    def test_model_str(self):
        question = create_question(question_text="Good question")
        choice = Choice(question=question, choice_text="Good answer", votes=0)
        assert choice.__str__() == "Good answer"
