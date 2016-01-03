from .adapters import Adaptation
from .conversation import Statement
from .utils.module_loading import import_module


class ChatBot(Adaptation):

    def __init__(self, name, **kwargs):
        super(ChatBot, self).__init__(**kwargs)

        kwargs["name"] = name
        self.recent_statements = []

        storage_adapter = kwargs.get("storage_adapter",
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )

        logic_adapter = kwargs.get("logic_adapter",
            "chatterbot.adapters.logic.ClosestMatchAdapter"
        )

        logic_adapters = kwargs.get("logic_adapters", [
            logic_adapter
        ])

        io_adapter = kwargs.get("io_adapter",
            "chatterbot.adapters.io.TerminalAdapter"
        )

        PluginChooser = import_module("chatterbot.adapters.plugins.PluginChooser")
        self.plugin_chooser = PluginChooser(**kwargs)

        self.add_adapter(storage_adapter, **kwargs)
        self.add_adapter(io_adapter, **kwargs)

        for adapter in logic_adapters:
            self.add_adapter(adapter, **kwargs)

        self.storage.set_context(self)
        self.logic.set_context(self)
        self.io.set_context(self)

    @property
    def storage(self):
        return self.storage_adapters[0]

    @property
    def io(self):
        return self.io_adapters[0]

    def get_last_statement(self):
        """
        Return the last statement that was received.
        """
        if self.recent_statements:
            return self.recent_statements[-1]
        return None

    def get_input(self):
        return self.io.process_input()

    def get_response(self, input_text):
        """
        Return the bot's response based on the input.
        """
        input_statement = Statement(input_text)

        # Applying plugin logic to see whether the chatbot should respond in this way
        plugin_response = self.plugin_chooser.choose(input_statement)

        if not plugin_response is False:
            return self.io.process_response(Statement(plugin_response))

        # Select a response to the input statement
        confidence, response = self.logic.process(input_statement)

        existing_statement = self.storage.find(input_statement.text)

        if existing_statement:
            input_statement = existing_statement

        previous_statement = self.get_last_statement()

        if previous_statement:
            input_statement.add_response(previous_statement)

        # Update the database after selecting a response
        self.storage.update(input_statement)

        self.recent_statements.append(response)

        # Process the response output with the IO adapter
        return self.io.process_response(response)

    def train(self, conversation=None, *args, **kwargs):
        """
        Train the chatbot based on input data.
        """
        from .training import Trainer

        trainer = Trainer(self.storage)

        if isinstance(conversation, str):
            corpora = list(args)
            corpora.append(conversation)

            if corpora:
                trainer.train_from_corpora(corpora)
        else:
            trainer.train_from_list(conversation)

