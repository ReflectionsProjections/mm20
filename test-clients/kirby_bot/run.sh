#!/bin/bash
if hash python2 2>/dev/null; then
        python2 kirby_bot.py
    else
        python kirby_bot.py
    fi
