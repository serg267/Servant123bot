FROM python:3.10

WORKDIR .

COPY requirements.txt requirements.txt

ENV TZ Europe/Moscow

RUN pip install redis

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]