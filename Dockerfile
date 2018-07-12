FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt
CMD [ "python", "./access_log_parser.py" ]
