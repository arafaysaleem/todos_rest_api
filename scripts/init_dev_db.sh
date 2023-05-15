#!/bin/sh
PIPENV_DOTENV_LOCATION='envs/.env.dev' pipenv run flask db init
PIPENV_DOTENV_LOCATION='envs/.env.dev' pipenv run flask db migrate
PIPENV_DOTENV_LOCATION='envs/.env.dev' pipenv run flask db upgrade
read