FROM python:3.9.16-slim as base

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt


###### local ############
FROM base as local

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

###### production #######
FROM base as production

COPY src .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
