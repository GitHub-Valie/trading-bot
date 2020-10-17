FROM python:3

ADD *.py /

ADD requirements.txt ./

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]