from chatterbot.adapters.storage import StorageAdapter
from chatterbot.adapters.exceptions import EmptyDatabaseException
from chatterbot.conversation import Statement, Response
from pymongo import MongoClient


class MongoDatabaseAdapter(StorageAdapter):

    def __init__(self, **kwargs):
        super(MongoDatabaseAdapter, self).__init__(**kwargs)

        self.database_name = self.kwargs.get("database", "chatterbot-database")

        # Use the default host and port
        self.client = MongoClient()

        # Specify the name of the database
        self.database = self.client[self.database_name]

        # The mongo collection of statement documents
        self.statements = self.database['statements']

    def count(self):
        return self.statements.count()

    def find(self, statement_text):
        values = self.statements.find_one({'text': statement_text})

        if not values:
            return None

        del(values['text'])

        # Build the objects for the response list
        response_list = self._objectify_response_list(
            values["in_response_to"]
        )
        values["in_response_to"] = response_list

        return Statement(statement_text, **values)

    def _objectify_response_list(self, response_list):
        """
        Takes the list of response items and returns the
        list converted to object versions of the responses.
        """
        in_response_to = []

        for item in response_list:
            text = item[0]
            occurrence = item[1]

            in_response_to.append(
                Response(text, occurrence=occurrence)
            )

        return in_response_to

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        filter_parameters = kwargs.copy()
        contains_parameters = {}

        # Exclude special arguments from the kwargs
        for parameter in kwargs:
            if "__" in parameter:
                del(filter_parameters[parameter])

                kwarg_parts = parameter.split("__")

                if kwarg_parts[1] == "contains":
                    key = kwarg_parts[0]
                    value = kwargs[parameter]
                    contains_parameters[key] = {'$elemMatch': {'$elemMatch': {'$in':[value]}}}

        filter_parameters.update(contains_parameters)

        matches = self.statements.find(filter_parameters)
        matches = list(matches)

        results = []

        for match in matches:
            statement_text = match['text']
            del(match['text'])
            results.append(Statement(statement_text, **match))

        return results

    def update(self, statement):
        # Do not alter the database unless writing is enabled
        if not self.read_only:
            data = statement.serialize()

            # Remove the text key from the data
            self.statements.update({'text': statement.text}, data, True)

            # Make sure that an entry for each response is saved
            for response_statement in statement.in_response_to:
                response = self.find(response_statement.text)
                if not response:
                    response = Statement(response_statement.text)
                    self.update(response)

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from random import randint

        count = self.count()

        random_integer = randint(0, count -1)

        if self.count() < 1:
            raise EmptyDatabaseException()

        statement = self.statements.find().limit(1).skip(random_integer)

        values = list(statement)[0]
        statement_text = values['text']

        del(values['text'])
        return Statement(statement_text, **values)

    def drop(self):
        """
        Remove the database.
        """
        self.client.drop_database(self.database_name)

