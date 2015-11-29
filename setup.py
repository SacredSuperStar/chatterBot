#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

req = open("requirements.txt")
requirements = req.readlines()

# Dynamically retrieve the version information from the chatterbot module
version = __import__('chatterbot').__version__
maintainer = __import__('chatterbot').__maintainer__
maintainer_email = __import__('chatterbot').__email__

setup(
    name="ChatterBot",
    version=version,
    url="https://github.com/gunthercox/ChatterBot",
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='readme.md',
    description="An open-source chat bot program written in Python.",
    author=maintainer,
    author_email=maintainer_email,
    packages=find_packages(),
    package_dir={"chatterbot": "chatterbot"},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    platforms=["any"],
    keywords=["ChatterBot", "chatbot", "chat", "bot"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    test_suite="tests",
    tests_require=[]
)
