![ChatterBot: Machine learning in Python](https://i.imgur.com/b3SCmGT.png)

## How it works

An untrained instance of ChatterBot starts off with no knowledge of how to communicate. Each time a user enters a statement, the library saves the text that they entered and the text that the statement was in response to. As ChatterBot receives more input the number of responses that it can reply and the accuracy of each response in relation to the input statement increase. The program selects the closest matching response by searching for the closest matching known statement that matches the input, it then returns the most likely response to that statement based on how frequently each response is issued by the people the bot communicates with.

## Installation

This package can be installed from [PyPi](https://pypi.python.org/pypi/ChatterBot) by running:

```
pip install chatterbot
```

## Basic Usage

```
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('Ron Obvious')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

# Get a response to an input statement
chatbot.get_response("Hello, how are you today?")
```

# Training data

ChatterBot comes with a data utility module that can be used to train chat bots.
At the moment there is training data for over a dozen languages in this module.
Contributions of additional training data or training data
in other languages would be greatly appreciated. Take a look at the data files
in the [chatterbot-corpus](https://github.com/gayanMatch/chatterbot-corpus)
package if you are interested in contributing.

```
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train based on the english corpus
trainer.train("chatterbot.corpus.english")

# Train based on english greetings corpus
trainer.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
trainer.train("chatterbot.corpus.english.conversations")
```

**Corpus contributions are welcome! Please make a pull request.**

# [Documentation](https://chatterbot.readthedocs.io/)

View the [documentation](https://chatterbot.readthedocs.io/)
for ChatterBot on Read the Docs.

To build the documentation yourself using [Sphinx](http://www.sphinx-doc.org/), run:

```
sphinx-build -b html docs/ build/
```

# Examples

For examples, see the [examples](https://github.com/gayanMatch/ChatterBot/tree/master/examples)
directory in this project's git repository.

There is also an example [Django project using ChatterBot](https://github.com/gayanMatch/ChatterBot/tree/master/examples), as well as an example [Flask project using ChatterBot](https://github.com/chamkank/flask-chatterbot).

# History

See release notes for changes https://github.com/gayanMatch/ChatterBot/releases

# Development pattern for contributors

1. [Create a fork](https://help.github.com/articles/fork-a-repo/) of
   the [main ChatterBot repository](https://github.com/gayanMatch/ChatterBot) on GitHub.
2. Make your changes in a branch named something different from `master`, e.g. create
   a new branch `my-pull-request`.
3. [Create a pull request](https://help.github.com/articles/creating-a-pull-request/).
4. Please follow the [Python style guide for PEP-8](https://www.python.org/dev/peps/pep-0008/).
5. Use the projects [built-in automated testing](https://chatterbot.readthedocs.io/en/latest/testing.html).
   to help make sure that your contribution is free from errors.

# License

ChatterBot is licensed under the [BSD 3-clause license](https://opensource.org/licenses/BSD-3-Clause).
