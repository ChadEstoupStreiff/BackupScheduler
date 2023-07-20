FROM python:3.8-slim-buster

# UPDATE
RUN pip install --upgrade pip
RUN apt-get update -y
RUN apt-get upgrade -y


# DEPENDENCIES
WORKDIR /

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# APP
COPY src /app

# ENTRYPOINTS
ENTRYPOINT ["python"]
CMD ["/app/main.py"]