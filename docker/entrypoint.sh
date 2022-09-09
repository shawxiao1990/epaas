#!/bin/sh
set -e

envsubst '
$$FLASK_CONFIG
$$FLASK_APP
' < /app/env.template > /app/.env

if [[ ! -f migrations/versions/*.py ]]; then
    pipenv run flask init
else
    #pipenv run flask db init

    #pipenv run flask db migrate -m "init-epaas"

    pipenv run flask db upgrade
fi

pipenv run gunicorn --workers=1 --threads=1 --bind=0.0.0.0:${PORT} --timeout 1800 '${FLASK_APP}:create_app()'