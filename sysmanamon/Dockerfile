# Dockerfile for the system management and monitoring

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD ./sysmanamon ./sysmanamon
ADD ./libs ./libs
WORKDIR /app/sysmanamon

EXPOSE 8080

CMD [ "python", "app.py", "runserver" ]

