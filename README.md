# Gpt-django

It's some sort of pet-project. The main purpose is to give access to interaction with ChatGPT for my friends and relatives.
So it's actualy simple django project with templates. 

At this moment it's hosted on https://urf4cknmt.space

# What's next?

It would be great to keep Django just as backend using DRF and create some modern frontend with React/Vue/Svelte. 
I'm kinda lame in frontend stuff, so I've made it with ChatGPT and I know it looks ugly 😅

Feel free to make pull requests if you have any enhancement both for backend and frontend parts.

# Django project

This project is bootstrapped using [fandsdev/django](http://github.com/fandsdev/django) template.

## Project structure

The main django app is called `app`. It contains `.env` file for django-environ. For examples see `src/app/.env.ci`. Here are some usefull app-wide tools:
* `app.admin` — app-wide django-admin customizations (empty yet), check out usage [examples](https://github.com/f213/django/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/app/admin)
* `app.test.api_client` (available as `api` and `anon` fixtures within pytest) — a [convinient DRF test client](https://github.com/f213/django/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/src/users/tests/tests_whoami.py#L6-L16).

Django user model is located in the separate `users` app.

Also, feel free to add as much django apps as you want.

## Installing on a local machine
This project requires python 3.11. Deps are managed by [pip-tools](https://github.com/jazzband/pip-tools)

### If you prefer develop from venv

Create venv and install requirements:

```bash
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install --upgrade pip pip-tools
$ make
```

Run the server:

```bash
$ cp .env.example .env  # default environment variables
$ cd src && cp app/.env.ci app/.env  # default environment variables
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver
```

### If you prefer develop from container

Run the docker-compose:

```bash
$ cp .env.example .env  # default environment variables
$ cd src && cp app/.env.ci app/.env  # default environment variables
$ docker-compose up -d
$ docker-compose exec app bash
$ ./manage.py createsuperuser
```
There is volume between your and container src directories, so just do what you want.

Don't forget to run tests inside app container in such case.


### Testing:
```bash
# run formatter
$ make fmt

# run lint
$ make lint

# run unit tests
$ make test
```

Development servers:

```bash
$ ./manage.py runserver

```

## Backend Code requirements

### Style

* Obey [django's style guide](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/#model-style).
* Configure your IDE to use [flake8](https://pypi.python.org/pypi/flake8) for checking your python code. To run our linters manualy, do `make lint`
* Prefer English over your native language in comments and commit messages.
* Commit messages should contain the unique id of issue they are linked to (refs #100500)
* Every model, service and model method should have a docstring.

### Code organisation

* KISS and DRY.
* Obey [django best practices](http://django-best-practices.readthedocs.io/en/latest/index.html).
* **No logic is allowed within the views or serializers**. Only services and models. When a model grows beyond 500 lines of code — go create some services.
* Use PEP-484 [type hints](https://www.python.org/dev/peps/pep-0484/) when possible.
* Prefer composition over inheritance.
* Never use [signals](https://docs.djangoproject.com/en/dev/topics/signals/) or [GenericRelations](https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/) in your own code.
* No l10n is allowed in python code, use [django translation](https://docs.djangoproject.com/en/dev/topics/i18n/translation/).
