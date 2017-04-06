FROM debian:stable

RUN apt-get update \
 && apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-setuptools \
    apache2 \
    apache2-prefork-dev \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    python-mysqldb

RUN pip install \
    mod_wsgi \
    Flask==0.11.1 \
    Flask-SQLAlchemy==2.1 \
    Flask-WTF==0.12 \
    WTForms==2.1 \
    flask-cors==3.0.2

RUN apt-get clean
EXPOSE 80
ADD . /DGB
CMD /DGB/boot.sh
