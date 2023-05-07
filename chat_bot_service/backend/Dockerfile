FROM python:3.9.16-slim as base

WORKDIR /app


RUN apt-get update
RUN apt-get install python3-dev build-essential default-libmysqlclient-dev -y

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt


###### local ############
FROM base as local

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

###### production #######
FROM base as production

COPY src .
COPY secret.json .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
