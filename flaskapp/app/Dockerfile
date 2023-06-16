FROM ubuntu:22.04 
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo PyJWT 
RUN mkdir /app
RUN mkdir -p /app/data
COPY digitalAirlines.py /app/digitalAirlines.py
EXPOSE 5000 
WORKDIR /app
ENTRYPOINT ["python3", "-u", "digitalAirlines.py"]