FROM python:3

WORKDIR code

COPY . .

RUN pip install -r requirements.txt

CMD python3 -m nginxaccesslogparser --input $INPUT --thread $THREAD
