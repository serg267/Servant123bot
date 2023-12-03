FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install redis

RUN pip install -r requirements.txt

COPY app .

CMD ["python", "main.py"]