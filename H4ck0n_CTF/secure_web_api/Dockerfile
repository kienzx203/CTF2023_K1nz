FROM node:17

WORKDIR /app

COPY ./package.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Run both node start-secure-backend and start-public-app using bash
CMD ["bash", "-c", "npm run start-secure-backend & npm run start-public-app"]