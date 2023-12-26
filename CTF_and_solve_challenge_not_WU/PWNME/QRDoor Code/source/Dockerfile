FROM node:16-alpine

WORKDIR /usr/src/app
COPY package*.json ./
RUN echo 'ISP{hello}'> flag.txt
RUN apk update && apk upgrade
RUN apk add fortune

RUN npm install
COPY . .

CMD [ "node", "src/index.js" ]