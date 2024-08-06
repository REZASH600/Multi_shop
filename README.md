# Multi Shop

## Overview

This project is a Django-based application with various components managed via Docker Compose. The key services include a database, message broker, background task processing, and result storage.

## Components

- **Main Project**: Accessible on port `8000`.
- **Flower**: Monitoring tool for Celery, accessible at `localhost:5555`.
- **RabbitMQ**: Message broker, accessible at `localhost:15672`.

## Docker Compose

Docker Compose is used to set up and manage the following services:

- **Postgres**: Database for the project.
- **RabbitMQ**: Message broker for handling tasks.
- **Celery**: For background task processing, with results stored in **Redis**.
- **Redis**: Backend for Celery, used to store task results.

## Setup

To start the services, run:

```bash
docker-compose up --build
```



## Environment Setup

This project uses a `.env` file to manage sensitive settings and environment variables. To set up the project, follow these steps:

1. Create a `.env` file in the root directory of the project.
2. Define the necessary environment variables in the `.env` file. For example:

```plaintext
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=securepassword
DEBUG=False
SECRET_KEY=your_secret_key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 .yourdomain.com

POSTGRES_USER=dbuser
POSTGRES_PASSWORD=dbpassword
POSTGRES_DB=your_database

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=your_database
SQL_USER=dbuser
SQL_PASSWORD=dbpassword
SQL_HOST=db
SQL_PORT=5432

CELERY_BROKER_URL=amqp://user:password@rabbitmq:5672/
CELERY_RESULT_BACKEND=redis://:password@redis:6379/0
```

## ERD file
To view the Entity-Relationship Diagram (ERD) for this project, you can [click here](https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=project%20django#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1_m-yhhjArt8Er5pKhOZtzRFo43Q_h5J6%26export%3Ddownload).

