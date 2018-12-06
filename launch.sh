#!/bin/bash

## run reddit bot in the background
python3 ./code/redditBot.py &

## run flask app in the foreground
python3 ./code/front_end.py