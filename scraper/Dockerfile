# Dockerfile for the scraper

FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD ./datasets ./datasets
ADD ./scraper ./scraper
ADD ./libs ./libs
ADD ./extensions ./extensions
WORKDIR /app/scraper

EXPOSE 8086

CMD [ "python", "app.py", "runserver" ]