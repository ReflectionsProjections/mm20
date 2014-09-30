#!/bin/bash
make clean
make
# valgrind --leak-check=full ./client
./client