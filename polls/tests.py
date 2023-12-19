from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question  # Assuming Question is in models.py of the same app

class QuestionModelTests(TestCase):
    # Test case for a question that has a future publication date
    def test_was_published_recetly_with_future_question(self):
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
    def test_was_published_recetly_with_recent_question(self):
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
