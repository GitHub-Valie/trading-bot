FROM python:3

RUN mkdir Bot

COPY Bot/*.py /

ADD requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]