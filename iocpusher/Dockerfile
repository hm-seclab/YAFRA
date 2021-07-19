# Dockerfile for the iocpusher

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD ./iocpusher ./iocpusher
ADD ./libs ./libs
ADD ./extensions ./extensions
ADD ./assets ./assets
ADD ./datasets ./datasets
WORKDIR /app/iocpusher

EXPOSE 8082

CMD [ "python", "app.py", "runserver" ]
