FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install psycopg2-binary && pip install -r backend/requirements.txt


ENTRYPOINT [ "python", "main.py" ]
