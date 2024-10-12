release: python manage.py migrate
web: gunicorn zenlearner.wsgi --log-file -
worker: celery -A zenlearner worker -l INFO --beat --concurrency 2
