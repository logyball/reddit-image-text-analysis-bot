#!/bin/bash

## check env vars
### REDDITBOT
[ -z "$SUBREDDIT" ] && SUBREDDIT="CHANGEME"
[ -z "$BOT_USERNAME" ] && BOT_USERNAME="CHANGEME"
[ -z "$BOT_PASSWORD" ] && BOT_PASSWORD="CHANGEME"
[ -z "$BOT_CLIENT_ID" ] && BOT_CLIENT_ID="CHANGEME"
[ -z "$BOT_CLIENT_SECRET" ] && BOT_CLIENT_SECRET="CHANGEME"
### SPOTIFY
[ -z "$SPOTIFY_CLIENT_ID" ] && SPOTIFY_CLIENT_ID="CHANGEME"
[ -z "$SPOTIFY_CLIENT_SECRET" ] && SPOTIFY_CLIENT_SECRET="CHANGEME"
### GIPHY
[ -z "$GIPHY_KEY" ] && GIPHY_KEY="CHANGEME"

## run reddit bot in the background
python3 ./code/redditBot.py &

## run flask app in the foreground
python3 ./code/front_end.py