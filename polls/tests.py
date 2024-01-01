from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime
from .models import Question, Choice

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    # Test case for a question that has a future publication date
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        # Set the publication date to 30 days in the future
        time = timezone.now() + datetime.timedelta(days=30)
        # Create a Question instance with the future publication date
        future_question = Question(pub_date=time)
        # Assert that was_published_recently() returns False
        self.assertIs(future_question.was_published_recently(), False)

    # Test case for a question that was published more than a day ago
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        # Set the publication date to just over 1 day in the past
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        # Create a Question instance with this publication date
        old_question = Question(pub_date=time)
        # Assert that was_published_recently() returns False
        self.assertIs(old_question.was_published_recently(), False)

    # Test case for a question that was published within the last day
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        # Set the publication date to less than 24 hours ago
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        # Create a Question instance with this recent publication date
        recent_question = Question(pub_date=time)
        # Assert that was_published_recently() returns True
        self.assertIs(recent_question.was_published_recently(), True)

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
        The results view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        """
        The results view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        past_question = create_question(question_text="Past question.", days=-30)
        Choice.objects.create(question=past_question, choice_text="Choice 1")  # Add choice to past question
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [past_question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        Choice.objects.create(question=question1, choice_text="Choice 1")  # Add choice to question1
        question2 = create_question(question_text="Past question 2.", days=-5)
        Choice.objects.create(question=question2, choice_text="Choice 2")  # Add choice to question2
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

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

    def test_no_choice_question(self):
        """
        Questions without choices are not displayed on the index page.
        """
        question = create_question(question_text="No choice question", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertNotIn(question, response.context["latest_question_list"])

    def test_question_with_choices(self):
        """
        Questions with choices are displayed on the index page.
        """
        question = create_question(question_text="Question with choices", days=-1)
        Choice.objects.create(question=question, choice_text="Choice 1")
        response = self.client.get(reverse("polls:index"))
        self.assertIn(question, response.context["latest_question_list"])