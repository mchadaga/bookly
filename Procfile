release: python manage.py migrate
web: gunicorn hookbook.wsgi --log-file -
worker: celery -A hookbook worker -l INFO --beat --concurrency 2
