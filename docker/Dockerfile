FROM python:3.9-buster

# install
RUN pip3 install pipenv
RUN apt-get update && apt-get install -y vim

COPY /epaas /app/epaas
COPY /docker/entrypoint.sh /app/entrypoint.sh
COPY /Pipfile /app/Pipfile
COPY /Pipfile.lock /app/Pipfile.lock

WORKDIR /app/
#RUN export LC_ALL=en_US.utf8  && export LANG=en_US.utf8
RUN pipenv install setuptools==57.5.0

ENTRYPOINT ["bash", "./entrypoint.sh"]