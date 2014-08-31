#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Usage: $0 turn_number (if zero if provided it will show the connection informaiton)"
  exit 0
fi
let turn=$1+1
head -n $turn serverlog.json | tail -n 1 | python -m json.tool | less
