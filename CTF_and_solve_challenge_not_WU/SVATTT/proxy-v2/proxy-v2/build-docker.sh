#!/bin/bash
docker rm -f proxy-v2-web
docker rmi -f proxy-v2
docker build -t proxy-v2 .
docker run --rm -d -p 9011:1337 --name=proxy-v2-web proxy-v2