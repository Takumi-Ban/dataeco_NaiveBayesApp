FROM python:3.9

# mecabの導入
RUN apt-get -y update && \
  apt-get -y upgrade && \
  apt-get install -y mecab && \
  apt-get install -y libmecab-dev && \
  apt-get install -y mecab-ipadic-utf8 && \
  apt-get install -y git && \
  apt-get install -y make && \
  apt-get install -y curl && \
  apt-get install -y xz-utils && \
  apt-get install -y file && \
  apt-get install -y sudo

# mecab-ipadic-NEologdのインストール
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
  cd mecab-ipadic-neologd && \
  ./bin/install-mecab-ipadic-neologd -n -y && \
  echo dicdir = `mecab-config --dicdir`"/mecab-ipadic-neologd">/etc/mecabrc && \
  sudo cp /etc/mecabrc /usr/local/etc && \
  cd

RUN mkdir workdir
WORKDIR /workdir
COPY app/ /workdir

ENV TZ Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

RUN apt-get install -y postgresql
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install psycopg2-binary
RUN pip install mecab-python3
RUN pip install sqlalchemy
RUN pip install flask-sqlalchemy
RUN pip install flask-migrate
RUN pip install flask-login
RUN pip install flask-wtf
RUN pip install flask-bootstrap
RUN pip install numpy
RUN pip install pandas
RUN pip install matplotlib
RUN pip install sklearn

RUN apt-get autoremove -y