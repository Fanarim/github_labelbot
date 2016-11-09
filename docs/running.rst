.. _running:

Running
-------

Labelbot can be run in two modes - console and web. Console mode allows periodic
labeling in given interval. All issues and repositories are being rechecked.
Since web mode analyzes only new issues or issues with new comments, web mode
is the recommended mode. However, unlike console, the web created in web mode
needs to be hosted publicly and accessible using internet.

Most of the parameters have to be setup no matter of what mode you're going to
use:

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


Console mode
~~~~~~~~~~~~

Additional parameters for console mode can be described using
``labelbot console --help``:

::

  $ labelbot console --help
  Usage: labelbot console [OPTIONS] REPO_URLS...

    Runs LabelBot in console mode

  Options:
    -i, --interval INTEGER  time interval in seconds in which to check issues
    --help                  Show this message and exit.


Web mode
~~~~~~~~
Web mode has no additional command line parameters, but ``WEBHOOK_TOKEN``
variable has to be exported in the environment as described in
:ref:`configuration` section. Otherwise, deployment options for running the bot
in Heroku are set in the ``Procfile`` file.

.. _Webhooks Settings page: https://github.com/Fanarim/github_labelbot/settings/hooks
