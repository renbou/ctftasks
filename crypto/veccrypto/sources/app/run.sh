#!/bin/sh
while true; do
    socat tcp-l:12345,reuseaddr,fork,crlf exec:"python3 ./main.py",pty,ctty,echo=0;
    sleep 10;
    done
