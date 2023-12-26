# docker build -t trusted-shop . -f Containerfile && docker run -p 8000:8000 trusted-shop

FROM ghcr.io/puppeteer/puppeteer

WORKDIR /app

USER root
RUN mkdir -p /app/storage/db
RUN chown pptruser /app

COPY package.json package-lock.json /app/

USER pptruser
RUN npm ci

COPY index.ts tsconfig.json /app/
COPY static /app/static
COPY prisma /app/prisma
COPY storage/db/dev.db /app/storage/db/dev.db

RUN npx prisma generate

EXPOSE 8000

CMD ["npm", "start"]
