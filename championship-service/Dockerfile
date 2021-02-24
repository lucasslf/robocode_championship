# pull official base image
FROM python:3.8-slim

# Add gcc for python libraries and add mime-support to support extra mime-types in python
RUN apt-get update \
 && apt-get install gcc -y \
 && apt-get install mime-support -y \
 && apt-get clean

RUN mkdir /var/files

# set working directory
WORKDIR /code

# setting UTF-8 locale for python3
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# install app dependencies
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip \
 && pip install -r requirements.txt

# add app
COPY . ./

# start app
CMD ["gunicorn", "-b=0.0.0.0:8081", "--timeout=60", "--workers=1", "--preload", "championship_service.app:app"]

EXPOSE 8081