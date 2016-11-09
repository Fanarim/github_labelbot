.. _configuration:

Configuration
=============

Labelbot uses two configuration files, one for storing GitHub Access Token and
second one for storing labeling rules.

Configuring labels
~~~~~~~~~~~~~~~~~~

Labelbot needs a config file containing rules according to which it should add
labels to analyzed issues. The example rules files looks like this:

::

  .*README.*::Documentation
  file::Test
  foo::bar

First item in each line is a python regular expression or simply a string. The
second item is a label name to be added to the issue.

.. note::

  Setting label colors is planned, but currently not possible.

Configuration file can be placed anywhere as long it is accessible by Labelbot.
Also it is necessary to pass to Labelbot using ``-u, --rules-file`` option. In
case this option is not specified, example config file is created and used. This
file is stored in user configuration directory, for example on Linux
in ``~/.config`` directory. It can be directly edited.

.. note::

  For rules configuration file change to take effect, Labelbot needs to be
  restarted.

Obtaining and configuring GitHub Token
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run your own instance of Labelbot, you will need a Personal GitHub Access
Token which will allow your bot to use `GitHub API`_. For this purpose, we advise
registering a new GitHub bot user. Such user is not different in any mean, but
it will allow you to manage which repositories should be labeled or not.

.. _GitHub API: https://developer.github.com/v3/

.. note::

  Bot users should be clearly marked as bots (you can use
  'About me' section) and should point to accounts of their owners. This will
  prevent you from your bot account being deleted as a duplicate account.

Once you've created your bot account and logged in to GitHub, navigate to
`Personal access tokens`_ settings page. Select 'Generate new token' and tick
'Repo' scope in the displayed form. Fill in token description and submit the
token generation. After that, copy the generated token - it won't be visible
again!

.. _Personal access tokens: https://github.com/settings/tokens

Once you have your token, you can pass it to Labelbot using ``-g, --github-token``.
Alternatively you can save it to a configuration file and pass it's path to Labelbot
using ``-t, --token-file``. Also, you can export ``GITHUB_TOKEN`` environment
variable or rewrite default configuration file in user configuration directory.
On Linux, that means ``~/config``.

Setting up GitHub webhook
~~~~~~~~~~~~~~~~~~~~~~~~~

Labelbot can run in two modes - console and web
(See :ref:`deployment-and-running`). Web mode allows the Labelbot to react
to changes in repositories in real-time and also reduces the overall load of
the Labelbot. However, additional configuration is required.

Labelbot in web mode uses `GitHub Webhooks`_ functionality. For details on how
to deploy Labelbot in web mode, see :ref:`deployment-and-running`. This chapter
describes the steps needed for Webhook configuration.

To setup your own webhook, following steps are required:

1. Add your GitHub bot user as an collaborator to the project you want to label.

2. Create a new webhook in `Webhooks Settings page`_ in your repo with your
   hook's Payload URL (e.g. https://labelbot-api.herokuapp.com/hook) and
   ``issues`` and ``issue comment`` events allowed.

3. Set ``WEBHOOK_TOKEN`` environment variable in your deployment environment
   corresponding to the secret token you used during webhook creation.

.. _Webhooks Settings page: https://github.com/Fanarim/github_labelbot/settings/hooks


.. _GitHub Webhooks: https://developer.github.com/webhooks/
