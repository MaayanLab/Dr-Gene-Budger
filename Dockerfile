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
    SQLAlchemy==1.0.13 \
    Flask-SQLAlchemy==2.1 \
    Flask-Bootstrap==3.3.6.0 \
    Flask-WTF==0.12
    pandas==0.18.1 \
    WTForms==2.1




RUN apt-get clean

EXPOSE 80

ADD . /DGB

CMD /DGB/boot.sh