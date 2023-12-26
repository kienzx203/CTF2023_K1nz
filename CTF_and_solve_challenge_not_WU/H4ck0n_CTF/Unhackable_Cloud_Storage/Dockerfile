FROM node

WORKDIR /app

COPY ./package.json ./

RUN npm install

COPY . .

ENV ADMIN_PASSWORD=123

EXPOSE 7500

CMD ["npm", "start"]