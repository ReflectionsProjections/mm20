#!/bin/bash
if hash python2 2>/dev/null; then
        python2 test_client.py
    else
        python test_client.py
    fi
