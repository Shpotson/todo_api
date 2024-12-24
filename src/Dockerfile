FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y python3 --version
RUN apt-get install -y python3-dev --version
RUN apt-get install --assume-yes python3-pip
COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages
COPY ../ ../src
RUN apt-get install -y sqlite3 libsqlite3-dev
VOLUME /app/data
RUN /usr/bin/sqlite3 /app/data/data.db
ENTRYPOINT /bin/bash && cd src && uvicorn main:app --host 0.0.0.0 --port 80