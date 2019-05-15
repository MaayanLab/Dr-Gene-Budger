FROM debian:stable

RUN apt-get update \
 && apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-setuptools \
    apache2 \
    apache2-dev \
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
    flask-cors==3.0.2 \
    pandas==0.23.3 \
    xlsxwriter==1.0.5

RUN apt-get clean

ENV BASE_URL = ""
ENV SECRET_KEY ""
ENV DATABASE ""

EXPOSE 80
ADD . /DGB
CMD /DGB/boot.sh
