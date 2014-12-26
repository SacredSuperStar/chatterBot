from .base_case import ChatBotTestCase
from chatterbot.algorithms.engram import engram


class EngramTests(ChatBotTestCase):

    def test_exact_results(self):

        output = engram("What... is your quest?", self.chatbot.log_directory)
        expected = "To seek the Holy Grail."

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].text, expected)

    def test_close_results(self):

        output = engram("What is your quest?", self.chatbot.log_directory)
        expected = "To seek the Holy Grail."

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].text, expected)

    def test_empty_input(self):

        output = engram("", self.chatbot.log_directory)

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0].name, "Error")
