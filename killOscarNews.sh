#!/bin/bash

ps -ef | grep OscarNews.py | awk '{print $2}' | xargs kill -9
