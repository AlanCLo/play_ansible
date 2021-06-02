#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=app.py
export DATABASE_URI="$(cat config.json | grep DATABASE_URI | sed 's/.*DATABASE_URI"://;s/ //g;s/"//g')"

echo "app = ${FLASK_APP}"
echo "uri = ${DATABASE_URI}"


[ -f /var/www/demo/.venv/bin/activate ] && . /var/www/demo/.venv/bin/activate

[ ! -d migrations ] && flask db init

flask db migrate
flask db upgrade
