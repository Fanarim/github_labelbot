.. _deployment:

Deployment
======================

Currently, apart of running Labelbot localy, deploying on Heroku is the only
supported way. However, you can definitely deploy this app wherever
you want to.

Heroku deployment
-----------------

Labelbot repository already contains files needed by Heroku. The only additional
step apart of standart deployment process is to set following environment
variables in Heroku. You can do that using Heroku web management or using
Heroku toolbelt.

::

  WEBHOOK_TOKEN=webhook_token - GitHub webhook secret/token
  GITHUB_TOKEN=github_token - GitHub API token

Used variables are described in :ref:`configuration` section.
