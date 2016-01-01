from chatterbot.adapters.exceptions import EmptyDatasetException
from .base_match import BaseMatchAdapter

from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk import word_tokenize


class ClosestMeaningAdapter(BaseMatchAdapter):

    def __init__(self, **kwargs):
        super(ClosestMeaningAdapter, self).__init__(**kwargs)
        from nltk.data import find
        from nltk import download

        # Download data if needed

        try:
            find('wordnet.zip')
        except LookupError:
            download('wordnet')

        try:
            find('stopwords.zip')
        except LookupError:
            download('stopwords')

        try:
            find('punkt.zip')
        except LookupError:
            download('punkt')

    def get_tokens(self, text, exclude_stop_words=True):
        """
        Takes a string and converts it to a tuple
        of each word. Skips common stop words such
        as ("is, the, a, ...") is 'exclude_stop_words'
        is True.
        """
        lower = text.lower()
        tokens = word_tokenize(lower)

        # Remove any stop words from the string
        if exclude_stop_words:
            excluded_words = stopwords.words("english")

            tokens = set(tokens) - set(excluded_words)

        return tokens

    def get_similarity(self, string1, string2):
        """
        Calculate the similarity of two statements.
        This is based on the total similarity between
        each word in each sentence.
        """
        import itertools

        tokens1 = self.get_tokens(string1)
        tokens2 = self.get_tokens(string2)

        total_similarity = 0

        # Get the highest matching value for each possible combination of words
        for combination in itertools.product(*[tokens1, tokens2]):

            synset1 = wordnet.synsets(combination[0])
            synset2 = wordnet.synsets(combination[1])

            if synset1 and synset2:

                # Compare the first synset in each list of synsets
                similarity = synset1[0].path_similarity(synset2[0])

                if similarity:  
                    total_similarity = total_similarity + similarity

        return total_similarity

    def get(self, input_statement, statement_list=None):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.get_available_statements(statement_list)

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                return 0, self.context.storage.get_random()
            else:
                raise EmptyDatasetException

        # Get the text of each statement
        text_of_all_statements = []
        for statement in statement_list:
            text_of_all_statements.append(statement.text)

        # Check if an exact match exists
        if input_statement.text in text_of_all_statements:
            return 1, input_statement

        closest_statement = None
        closest_similarity = -1
        total_similarity = 0

        # For each option in the list of options
        for statement in text_of_all_statements:
            similarity = self.get_similarity(input_statement.text, statement)

            total_similarity += similarity

            if similarity > closest_similarity:
                closest_similarity = similarity
                closest_statement = statement

        confidence = closest_similarity / total_similarity

        return confidence, next((s for s in statement_list if s.text == closest_statement), None)

