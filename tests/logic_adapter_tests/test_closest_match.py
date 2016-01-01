from unittest import TestCase
from chatterbot.adapters.logic import ClosestMatchAdapter
from chatterbot.conversation import Statement, Response


class ClosestMatchAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestMatchAdapter()

    def test_no_choices(self):
        from chatterbot.adapters.exceptions import EmptyDatasetException

        possible_choices = []
        statement = Statement("What is your quest?")

        with self.assertRaises(EmptyDatasetException):
            self.adapter.get(statement, possible_choices)

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        possible_choices = [
            Statement("Who do you love?", in_response_to=[Response("I hear you are going on a quest?")]),
            Statement("What is the meaning of life?", in_response_to=[Response("Yuck, black licorice jelly beans.")]),
            Statement("I am Iron Man.", in_response_to=[Response("What... is your quest?")]),
            Statement("What... is your quest?", in_response_to=[Response("I am Iron Man.")]),
            Statement("Yuck, black licorice jelly beans.", in_response_to=[Response("What is the meaning of life?")]),
            Statement("I hear you are going on a quest?", in_response_to=[Response("Who do you love?")]),
        ]
        statement = Statement("What is your quest?")

        confidence, match = self.adapter.get(statement, possible_choices)

        self.assertEqual("What... is your quest?", match)

