release: python manage.py migrate
web: gunicorn healthmateai.wsgi:application --log-file -
worker: celery -A healthmateai worker --loglevel=info 