.. _installation:

Installation
============

To install the Labelbot, following steps are needed.

1. In case you don't want Labelbot to be installed to your whole system, create
a virtualenv:

::

  $ virtualenv venv -p python3

2a. Download the Labelbot from GitHub and install it using ``setup.py``:

::

  $ git clone https://github.com/Fanarim/github_labelbot
  $ cd github_labelbot
  $ ./setup.py install

2b. Install Labelbot using pip:

::

  $ python -m pip install --extra-index-url https://testpypi.python.org/pypi github-labelbot

3. You can now run the Labelbot:

::

  $ labelbot --help
  Usage: labelbot [OPTIONS] COMMAND [ARGS]...

  Options:
    -t, --token-file PATH     file containing GitHub token information
    -u, --rules-file PATH     file containing issues labeling rules
    -g, --github-token TEXT   github token used for authentication
    -d, --default-label TEXT  default label to use after no rule is matched
    -c, --check-comments      flag indicating comments should also be checked
    -s, --skip-labeled        skip labeling issues that already have any label
    --help                    Show this message and exit.

  Commands:
    console  Run console daemon periodically checking issues
    web      Run web API listening for issue updates
