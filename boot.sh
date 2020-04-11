#!/bin/sh
source env/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec python create_admin.py & gunicorn webapp:app -b :5555 -w 5
#exec gunicorn -b :5000 --access-logfile - --error-logfile - webapp:app
#exec gunicorn webapp:app -b 127.0.0.1:5000 -w 1
#exec gunicorn webapp:app -b :5000 -w 5
