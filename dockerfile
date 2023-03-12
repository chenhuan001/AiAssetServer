FROM python:3.7.13-buster

RUN apt-get update && apt-get -y install build-essential libsndfile1 ffmpeg libsm6 libxext6 \
    && apt-get clean

RUN apt-get -y install vim

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["sh", "bootstrap.sh"]