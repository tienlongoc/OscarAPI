#!/bin/bash

ps -ef | grep OscarAPI.py | awk '{print $2}' | xargs kill -9
echo Starting OscarAPI.py
nohup python $HOME/OscarAPI/OscarAPI.py >> log.txt 2>&1 &

