MANAGE = python manage.py

run:
	$(MANAGE) runserver

migrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

superuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

celery_worker:
	celery -A api_swipe worker --loglevel=info

celery_beat:
	celery -A api_swipe beat

dumpdata:
	$(MANAGE) dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > db.json

startapp:
	$(MANAGE) migrate --no-input
	$(MANAGE) init_script
	$(MANAGE) collectstatic --no-input
	gunicorn my_house24.wsgi:application --bind 0.0.0.0:8000