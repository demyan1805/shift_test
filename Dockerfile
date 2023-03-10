FROM python:3.9-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update
RUN apt-get install -y gcc
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./app ./app/
COPY ./tests ./tests/

ENV PYTHONPATH="${PYTHONPATH}:."

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
