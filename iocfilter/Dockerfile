# Dockerfile for the iocfilter

FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
ADD ./iocfilter ./iocfilter
ADD ./libs ./libs
WORKDIR /app/iocfilter

EXPOSE 8087

CMD [ "python", "app.py", "runserver" ]