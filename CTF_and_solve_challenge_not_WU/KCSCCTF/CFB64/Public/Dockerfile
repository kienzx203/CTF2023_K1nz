FROM python:3.10-buster

RUN apt-get update && apt-get install -yqq socat
RUN pip install pycryptodome

WORKDIR /home/chall

COPY . .

EXPOSE 60124

CMD socat -T 30 TCP-LISTEN:60124,reuseaddr,fork EXEC:"python chall.py"
