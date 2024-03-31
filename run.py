#!/usr/bin/env python
import typer
import os

from cliver.settings import config

from cliver.core.security import hash_password
from cliver.models import User, UserProfile


app = typer.Typer(
    invoke_without_command=True,
    no_args_is_help=True
)


# ================================= change this to adapt to your case 

@app.command()
def createsupermanager(username: str, email: str, password: str):
    """"Creates a new supermanager for global cliver administration"""
    
    user = User.query.create(  # type: ignore
        username=username,
        account_type=User.AccountType.MANAGER,
        role=User.Role.SUPERMANAGER,
        password=hash_password(password),
        email=email
    )

    UserProfile.objects.create(owner=user) # type: ignore

    typer.echo(f"New account created. {user.username=}, {user.id=}, {user.account_type=}, {user.email=}")
    

@app.command()
def setup_docker_database():
    """creates new docker postgres container for rapid test"""
    if config.in_devmode:
        os.system(
            'docker container run --name cliver-db '                                    
            '-e POSTGRES_PASSWORD=dbpassword '
            '-e POSTGRES_DB=cliver '
            '-e POSTGRES_USER=clii '
            '-p 5432:5432 '
            '-d postgres'
        )

@app.command()
def reset_database():
    """drop and create a new empty database using docker
    depends on database configuration to be has .env.exemple
    """
    if config.in_devmode:
        os.system(
            'docker exec -it cliver-db psql -U clii -d postgres -c "DROP DATABASE cliver;"'
        )
        os.system(
            'docker exec -it cliver-db psql -U clii -d postgres -c "CREATE DATABASE cliver;"'
        )


if __name__ == '__main__':
    app()
