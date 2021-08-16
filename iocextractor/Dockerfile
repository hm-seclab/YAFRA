# Dockerfile for the iocextractor

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"
ADD ./datasets ./datasets
ADD ./iocextractor ./iocextractor
ADD ./libs ./libs
ADD ./extensions ./extensions
WORKDIR /app/iocextractor
RUN mkdir /app/iocextractor/reports

EXPOSE 8081

CMD [ "python", "app.py", "runserver" ]
