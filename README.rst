.. image:: https://readthedocs.org/projects/github-labelbot/badge/?version=latest
   :target: http://github-labelbot.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Github Labelbot
===============

Configurable Github bot used for automatic issues labeling

Sample webhook is running at https://labelbot-api.herokuapp.com/ and
it's functionality can be tested in
https://github.com/Fanarim/github\_labelbot\_testrepo repository.

Documentation_ is available at Read The Docs.

.. _Documentation: http://github-labelbot.readthedocs.io/en/latest/


Configuration
-------------

TBA

Installation and running
------------------------

Clone the repo and install necessary packages:

::

  $ git clone https://github.com/Fanarim/github_labelbot
  $ virtualenv -p python3 venv
  $ source venv/bin/activate
  $ ./setup.py install

Alternativelly you can install Labelbot using pip:

::

  $ python -m pip install --extra-index-url https://testpypi.python.org/pypi github-labelbot


Now you can run the command:

``$ labelbot --help``

Heroku deployment
-----------------

While deploying the app on Heroku, following environment variables have
to be set:

::

    WEBHOOK_TOKEN=webhook_token - GitHub webhook secret/token
    GITHUB_TOKEN=github_token - GitHub API token

Documentation generation
------------------------

To regenerate the documentation, run the following commands:

::

    $ cd docs
    $ make html


About
-----

Github Labelbot is being developed as part of MI-PYT course at Faculty
of Information technology, Czech Technical University in Prague.
