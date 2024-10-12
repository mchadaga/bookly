# HookBook

HookBook uses AI to solve the attention span problem in K-12 education.

## Installation

1. Install Python3.9

2. Setup a virtualenv and install requirements
   (this example uses [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)):

```bash
mkvirtualenv hookbook -p python3.9
pip install -r requirements/dev-requirements.txt
```

If you are having issues with mkvirtualenv, run the below

```bash
python3.9 -m venv venv && source venv/bin/activate && pip install -r requirements/dev-requirements.txt
```

## Running server

```bash
./manage.py runserver
```

## Building front-end

To build JavaScript and CSS files, first install npm packages:

```bash
npm install
```

Then build (and watch for changes locally):

```bash
npm run dev-watch
```

## Running Celery

Celery can be used to run background tasks.

You can run it using:

```bash
celery -A hookbook worker -l INFO
```

Or with celery beat (for scheduled tasks):

```bash
celery -A hookbook worker -l INFO -B
```

## Updating translations

**Docker:**

```bash
make translations
```

**Native:**

```bash
./manage.py makemessages --all --ignore node_modules --ignore venv
./manage.py makemessages -d djangojs --all --ignore node_modules --ignore venv
./manage.py compilemessages
```

## Google Authentication Setup

To setup Google Authentication, follow the [instructions here](https://django-allauth.readthedocs.io/en/latest/providers.html#google).

## Installing Git commit hooks

To install the Git commit hooks run the following:

```shell
$ pre-commit install --install-hooks
```

Once these are installed they will be run on every commit.

For more information see the [docs](https://docs.saaspegasus.com/code-structure.html#code-formatting).

## Running Tests

To run tests:

```bash
./manage.py test
```

Or to test a specific app/module:

```bash
./manage.py test apps.utils.tests.test_slugs
```

On Linux-based systems you can watch for changes using the following:

```bash
find . -name '*.py' | entr python ./manage.py test apps.utils.tests.test_slugs
```



###Generating translations:

```bash
django-admin makemessages -l
```
