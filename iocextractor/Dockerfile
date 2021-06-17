# Dockerfile for the iocextractor

FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD ./iocextractor ./iocextractor
ADD ./libs ./libs
ADD ./extensions ./extensions
WORKDIR /app/iocextractor

EXPOSE 8081

CMD [ "python", "app.py", "runserver" ]
