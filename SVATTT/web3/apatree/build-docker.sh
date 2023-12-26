#!/bin/bash
docker rm -f apatree-web
docker rmi -f apatree
docker build -t apatree .
docker run -v $(pwd)/public_html:/var/www/html --rm -d -p 9008:80 --name=apatree-web apatree