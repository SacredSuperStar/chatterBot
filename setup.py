#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

history = open("history.rst").read().replace(".. :changelog:", "")

try:
    from pypandoc import convert
    readme = lambda f: convert(f, "rst")
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    readme = lambda f: open(f, "r").read()

requirements = [
    "fuzzywuzzy==0.3.2"
]

test_requirements = [
    "fuzzywuzzy==0.3.2"
]

setup(
    name="ChatterBot",
    version="0.0.4",
    description="An open-source chat bot program written in Python.",
    long_description=readme("readme.md") + "\n\n" + history,
    author="Gunther Cox",
    author_email="gunthercx@gmail.com",
    url="https://github.com/gunthercox/ChatterBot",
    packages=[
        "chatterbot",
        "chatterbot.algorithms",
        "chatterbot.apis",
        "chatterbot.cleverbot"
    ],
    package_dir={"chatterbot": "chatterbot"},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords = ["ChatterBot", "chatbot", "chat", "bot"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    test_suite="tests",
    tests_require=test_requirements
)
