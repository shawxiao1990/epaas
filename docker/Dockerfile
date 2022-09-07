FROM harbor.bingjunx.com/image-base/centos-official:7.8.2003-python3

# install
RUN pips install pipenv

COPY /epaas /app/run
COPY /docker/entrypoint.sh /app/entrypoint.sh
COPY /pipfile /app/pipfile

WORKDIR /app/

RUN pipenv install gunicorn && pipenv install

ENTRYPOINT ["./entrypoint.sh"]