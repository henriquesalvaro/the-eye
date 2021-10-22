# The Eye Backend - Django Application

## Requirements

- [Python 3.9](https://www.python.org)
- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose/)
- [Virtualenv](https://github.com/pypa/virtualenv/)
- [Git](https://git-scm.com/)

## Development (Local)

- Create the virtual environment and activate it

        virtualenv -p python3.9 venv
        source venv/bin/activate
- For macOS:
  - Install homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
  - Install basic macOS dependencies `brew install postgres cairo pango gdk-pixbuf libffi`
- For Linux:
  - Install basic Linux dependencies `apt-get update && apt-get install -y binutils libproj-dev gdal-bin`
- Install the requirements `pip install -r requirements-dev.txt`
- Install the pre-commit hooks `pre-commit install`
- Start the supporting containers `docker-compose up` with the database, localstack and redis
- Create a proper `.env` file
- Run the server with `python manage.py runserver 8000`
- Server can be accessed through `http://localhost:8000`
- Run tests with `ENVIRONMENT=test python manage.py test`

# Run containerized application locally

- Create a proper `.env` file
- Start the containers `docker-compose -f docker-compose-full.yml up`
- Run the migrations `docker-compose -f docker-compose-full.yml exec the-eye python manage.py migrate`
- Server can be accessed through `http://localhost:8000`

# .env file
You need a `.env`file with your environment variables, here's an example file:
```
LOAD_ENVS_FROM_FILE=True
ENVIRONMENT=development
SECRET_KEY='#*=The Eye Local Django=*#'
DATABASE_URL=postgres://postgres:postgres@localhost:5432/theeye
AWS_STORAGE_BUCKET_NAME=the-eye-local
SENTRY_DSN=
```
