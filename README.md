# Cliver, A FastAPI with Django ORM Template

> Hi, I'm currently looking for a new job opportunity. If you need a Python Backend Developer, contact me via email (**am@uhtred.dev**) or [LinkedIn](https://linkedin.com/in/uhtredmiller).

How about combining the high performance of FastAPI with the maturity and robustness of Django ORM? Maybe you've already thought about this. I really like Django's ORM, and I think I'm not the only one. That's why I decided to make this template that you can use as a base for your new projects.

In addition to the integration between FastAPI and Django ORM, this template also has a scalable structure and additional features, great for large projects. It's just my suggestion, you can change and shape it to better suit your particular case.

## Features and Stack

- [**FastAPI**](https://fastapi.tiangolo.com) for backend API.
- [**Django ORM**](https://docs.djangoproject.com/en/5.0/topics/db/queries/) for SQL database interactions.
- [**Pydantic**](https://docs.pydantic.dev) for the data validation and settings management.
- Secure password hashing with [**Argon 2**](https://github.com/hynek/argon2-cffi).
- JWT token authentication with [**python-jose**](https://github.com/mpdavis/python-jose).
- [**Typer**](https://typer.tiangolo.com/) for task running and management commands
- Django typing support with [django-stubs](https://github.com/typeddjango/django-stubs) and [mypy](https://mypy-lang.org/).

## See it working

The main objective of this template is for you to know how to integrate FastAPI and Django ORM in the same project. And also provide you with a base (opinionated) structure for a scalable project. So, the idea is that you review each file and not just put it to work.

But let's see this little template in action...

### Downloading and installing dependencies

In this template I'm using [poetry](https://python-poetry.org/) for dependency management, you need to have poetry along with `Python 3.12` installed on your machine. The total requirements are:

- Python 3.12
- [Poetry](https://python-poetry.org/) for dependency management
- [Docker](https://www.docker.com/) to run a PostgreSQL database

### Now, let's go step by step...

1. Open your terminal and clone this repository...

```sh
git clone https://github.com/uhttred/fastapi-with-django-orm-template.git
```

2. Go to project directory, install the dependencies and activate the poetry environment in terminal.

```sh
# got directory
cd fastapi-with-django-orm-template
# install dependencies
poetry install
# activate poetry local python environment in terminal
poetry shell
```

3. Configure `.env` file with at least with the required variables. See `.env.example` file to rapid know with variable are required. You can populate your own values or just copy all data in `.env.example` and paste to `.env` file. You can use the command `openssl rand -hex 32` on your terminal to generate a new random string to use as your `SECRET_KEY`. Your `.env` file shoul look like:

```env
DEBUG=True
ENV_MODE='development'
SECRET_KEY='7e40ec34da7249b7c28f048876576ad6a08df9ebcadcbe9610ec7cd24600ce3c'
DB_HOST='localhost'
DB_USERNAME='clii'
DB_PASSWORD='dbpassword'
DB_DB='cliver'
DB_PORT=5432
CORS_ALLOW_ORIGINS='*'
TIMEZONE='UTC'
```

4. Start a docker container for PostgreSQL database. Use the typer command to create the container anda the database with the credentials in `.env.example` file.

```sh
./run.py setup-docker-database
```

5. Run the miration and create the first user administration account.

```sh
# apply migration
./manage.py migrate
# create user account
./run.py createsupermanager uhtred my@email.com mypassword
```

You should receive a message like this:

```python
# New account created. user.username='uhtred', user.id=1, user.account_type=UserAccountType.MANAGER, user.email='my@email.com'
```

Now, everything should be ready for us to run the server and start testing the API. Start the server and then access your browser at `http://localhost:8000/docs` to see the available endpoints. And test it with your favorite client.

```sh
uvicorn cliver.main:app --reload	
```

---

You'll notice that I didn't provide much support for FastAPI's automatic interactive documentation generator. This is because I always design my API before I even start developing it.

Using tools like [Stoplight](https://stoplight.io/). Although FastAPI's interactive documentation is one of the framework's biggest differences, I personally don't benefit much from it. Sorry about that, but you may need to use a client like [Postman](https://www.postman.com/) or [Stoplight](https://stoplight.io/) to test the endpoints.