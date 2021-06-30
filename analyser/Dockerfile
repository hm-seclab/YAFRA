# Dockerfile for the analyser

FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD ./analyser ./analyser
ADD ./libs ./libs
ADD ./extensions ./extensions
WORKDIR /app/analyser

EXPOSE 8085

CMD [ "python", "app.py", "runserver" ]