.. _configuration:

Configuration
=============

Obtaining GitHub Access Token
-----------------------------

To run your own instance of Labelbot, you will need a Personal GitHub Access
Token which will allow your bot to use `GitHub API`_. For this purpose, we advise
registering a new GitHub bot user. Such user is not different in any mean, but
it will allow you to manage which repositories should be labeled or not.

.. _GitHub API: https://developer.github.com/v3/

.. note::

  Please note that bot users should be clearly marked as bots (you can use
  'About me' section) and should point to accounts of their owners. This will
  prevent your bot account being deleted as a duplicate account.

Once you've created your bot account and logged in to GitHub, navigate to
`Personal access tokens`_ settings page. Select 'Generate new token' and tick
'Repo' scope in the displayed form. Fill in token description and submit the
token generation. After that, copy the generated token - it won't be visible
again!

.. _Personal access tokens: https://github.com/settings/tokens

Once you have your token, save it to the configuration file or pass it to
Labelbot using ``-g`` option. For further details, see :ref:`configuration`.
