# Dockerfile for the iocpuller

FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD ./iocpuller ./iocpuller
ADD ./libs ./libs
WORKDIR /app/iocpuller

EXPOSE 8083

CMD [ "python", "app.py", "runserver" ]
