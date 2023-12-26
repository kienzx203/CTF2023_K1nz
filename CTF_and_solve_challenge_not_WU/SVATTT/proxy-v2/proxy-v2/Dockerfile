FROM python:3.8-slim-buster

WORKDIR /app

COPY ./src /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 1337 

CMD python app.py