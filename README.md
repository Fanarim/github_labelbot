# Github Labelbot
Configurable Github bot used for automatic issues labeling

## Configuration
TBA

## Installation and running
Clone the repo and install necessary packages:

```
$ git clone https://github.com/Fanarim/github_labelbot
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Now you can run the command:

`$ labelbot/run.py --help`


## Heroku deployment
While deploying the app on Heroku, following environment variables have to be set:

```
WEBHOOK_TOKEN=webhook_token - GitHub webhook secret/token
GITHUB_TOKEN=github_token - GitHub API token
```

## About
Github Labelbot is being developed as part of MI-PYT course at Faculty of Information technology, Czech Technical University in Prague.
