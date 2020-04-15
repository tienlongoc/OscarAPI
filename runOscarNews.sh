#!/bin/bash

ps -ef | grep OscarNews.py | awk '{print $2}' | xargs kill -9
echo Starting OscarNews.py
python $HOME/OscarAPI/OscarNews.py >> log.txt 2>&1 &

