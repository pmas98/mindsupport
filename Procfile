web: gunicorn mindsupport.wsgi --log-file -
worker: daphne -b 0.0.0.0 -p $PORT mindsupport.asgi:application
