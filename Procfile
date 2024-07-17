web: pipenv run celery -A app.worker.celery_app worker --loglevel=info & pipenv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
