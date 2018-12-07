#! /bin/bash

## check env vars
### REDDITBOT
[ -z "$SUBREDDIT" ] && export SUBREDDIT="CHANGEME"
[ -z "$BOT_USERNAME" ] && export BOT_USERNAME="CHANGEME"
[ -z "$BOT_PASSWORD" ] && export BOT_PASSWORD="CHANGEME"
[ -z "$BOT_CLIENT_ID" ] && export BOT_CLIENT_ID="CHANGEME"
[ -z "$BOT_CLIENT_SECRET" ] && export BOT_CLIENT_SECRET="CHANGEME"
### SPOTIFY
[ -z "$SPOTIFY_CLIENT_ID" ] && export SPOTIFY_CLIENT_ID="CHANGEME"
[ -z "$SPOTIFY_CLIENT_SECRET" ] && export SPOTIFY_CLIENT_SECRET="CHANGEME"
### GIPHY
[ -z "$GIPHY_KEY" ] && export GIPHY_KEY="CHANGEME"
### GOOGLE ML
[ -z "$GOOGLE_ACCOUNT_CREDENTIALS" ] && export GOOGLE_ACCOUNT_CREDENTIALS="PATH_TO_SERVICE_ACCT_JSON"

### install requirements
apt update && apt install python python-pip
pip install -r requirements.txt
nohup python ./code/main.py & 
nohup python ./code/front_end.py &
