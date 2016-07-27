#!/usr/bin/env bash

adduser --disabled-password --gecos '' r
cd /DGB/
mod_wsgi-express setup-server wsgi.py --port=80 --user r --group r --server-root=/etc/DGB --socket-timeout=600 --limit-request-body=524288000
chmod a+x /etc/DGB/handler.wsgi
chown -R r /DGB/DGB/static/
/etc/DGB/apachectl start
tail -f /etc/DGB/error_log