python3 manage.py collectstatic --noinput
daphne -b 0.0.0.0 polls_site.asgi:application