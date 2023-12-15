poetry install
poetry run gunicorn -w 4 -b 0.0.0.0:8000 'server:create_app()'
