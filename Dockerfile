FROM python:3.6
RUN mkdir /app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev 
RUN pip install --upgrade pip
COPY . /app
RUN pip install -r requirements.txt
