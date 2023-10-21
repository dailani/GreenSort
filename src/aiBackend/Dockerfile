FROM debian:stable

WORKDIR /root

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get upgrade -y --fix-missing
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y curl python3 git python3-pip libpq-dev python3-dev --fix-missing

COPY . .

RUN pip3 install -r requirements.txt --break-system-packages

ENTRYPOINT ["python3", "./app.py"]