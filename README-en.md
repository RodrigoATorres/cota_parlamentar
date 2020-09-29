# Installation

## Python packages
This project was configured making use of [Poetry](https://python-poetry.org/)

In order to install the dependencies, just type:
>poetry install

Inside the project directory

A "requirements.txt" contains the dependencies, as well, but is not guaranteed to be up to date.

# MongoDB

Docker-compose contains the recipes to Mongo-DB and Mongo-express


# Configuration
The file ".env" must be created on the project root folder. An example of the expected content of the file is provided on [".env.sample"](/.env.sample)

The only variable that needs to be changed is "ANTI_CAPTCH_API_KEY", which is the api key provided by [ANTI-CAPTCHA](https://anti-captcha.com/)

If your database will be open for the internet, change the other variables, as well.

# Features

Donwloading 