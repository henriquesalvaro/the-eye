#!/bin/bash
set -e

if [ "$1" = "manage" ]; then
    shift 1
    exec python manage.py "$@"

elif [ "$1" = "celery" ]; then
    # Start celery workers
    shift 1
    echo Starting celery workers
    exec celery -A the_eye worker -l INFO -Q "$@"

elif [ "$1" = "celerybeat" ]; then
    # Start celery beat
    echo Starting celery beat
    exec celery -A settings beat -l INFO

else
    if [ "$ENV" = "development" ] ; then
      exec python manage.py runserver 0.0.0.0:8000
    else
      python manage.py migrate                  # Apply database migrations
      python manage.py collectstatic --noinput  # Collect static files

      # Prepare log files and start outputting logs to stdout
      touch /usr/src/logs/gunicorn.log
      touch /usr/src/logs/access.log
      tail -n 0 -f /usr/src/logs/*.log &

      # Start Gunicorn processes
      echo Starting Gunicorn

      exec gunicorn settings.wsgi \
          --name the-eye-django \
          --bind 0.0.0.0:8000 \
          --workers 3 \
          --timeout 120 \
          --log-level=info \
          --log-file=/usr/src/logs/gunicorn.log \
          --access-logfile=/usr/src/logs/access.log \
          --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
          "$@"
    fi
fi
