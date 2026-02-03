## E-Commerce REST API

A production-ready e-commerce backend built with FastAPI, featuring authentication, carts, orders, reviews, database migrations, Dockerized infrastructure, and a fully automated CI pipeline with GitHub Actions.

This project demonstrates real-world backend engineering practices, including containerization, database-safe transactions, and continuous integration.

## Features

Authentication & Authorization

JWT-based authentication

Role-based access control (admin vs user)

Core E-commerce Functionality

Products & categories

Shopping cart management

Order creation with transactional safety

Product reviews

Database & Migrations

PostgreSQL with SQLAlchemy ORM

Alembic migrations for schema versioning

Safe, atomic order creation with rollback handling

Testing

Comprehensive Pytest suite

Coverage for auth, carts, orders, reviews

Race-condition handling during checkout

DevOps & CI/CD

Dockerized application and database

Docker Compose for local development

GitHub Actions CI pipeline:

Spins up PostgreSQL

Runs migrations

Executes tests

Builds Docker image

## Tech Stack

Backend: FastAPI, Python 3.11

Database: PostgreSQL

ORM: SQLAlchemy

Migrations: Alembic

Auth: JWT

Testing: Pytest

DevOps: Docker, Docker Compose

CI/CD: GitHub Actions

## Project Structure
``
├── app/
│   ├── routers/        # API route handlers
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── security.py     # Auth & JWT utilities
│   ├── database.py    # DB session & engine
│   └── main.py         # FastAPI app entry point
├── alembic/            # Database migrations
├── tests/              # Pytest test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/workflows/  # GitHub Actions CI
``
## Local Development (Docker)
Clone the repository
``
git clone https://github.com/<your-username>/ecommerce-api.git
cd ecommerce-api
``
Create environment variables
``
cp .env.example .env
``


Fill in values for:
``
DATABASE_URL
JWT_SECRET_KEY
``
Start the application
``
docker-compose up --build
``

The API will be available at:
``
http://localhost:8000
``

Interactive API docs:
``
http://localhost:8000/docs
``
Database Migrations

Run migrations inside the API container:
``
docker-compose exec api alembic upgrade head
``
Running Tests

Tests are executed automatically in CI, but you can run them locally:
``
pytest
``
## Continuous Integration

This repository includes a GitHub Actions CI pipeline that runs on every push and pull request:

Starts a temporary PostgreSQL service

Installs dependencies

Runs database migrations

Executes the full Pytest suite

Builds the Docker image

This ensures all changes are safe, tested, and deployable.

## Security Practices

Secrets managed via environment variables

.env excluded from version control

.env.example provided for setup guidance

No credentials committed to the repository


