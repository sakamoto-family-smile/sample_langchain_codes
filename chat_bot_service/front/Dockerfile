FROM python:3.9.16-slim as base

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt


###### local ############
FROM base as local

CMD ["streamlit", "run", "/app/src/main.py"]

###### production #######
FROM base as production

COPY src .
EXPOSE 8501
CMD ["streamlit", "run", "/app/src/main.py"]
