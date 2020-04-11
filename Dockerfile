FROM python:3.7-alpine

RUN adduser -D socrat_user
WORKDIR /home/socrat_user
COPY requirements.txt requirements.txt

RUN python -m venv env
RUN \
 apk add --no-cache postgresql-libs libffi-dev make && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN env/bin/pip install -r requirements.txt

COPY myapp myapp
COPY migrations migrations

COPY webapp.py boot.sh ./
COPY create_admin.py create_db.py ./

RUN chmod +x boot.sh

RUN chown -R socrat_user:socrat_user ./
USER socrat_user

EXPOSE 5555
ENTRYPOINT ["./boot.sh"]
