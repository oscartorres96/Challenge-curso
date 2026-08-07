# Notifications API

## Description
**Basic notification management system for authenticated users.** It allows users to register with an email address and password, create notifications through three different delivery channels (Email, SMS, and Push Notifications), and retrieve their own notifications. The system is designed with an extensible architecture, making it easy to add new notification channels in the future.

## Main Features
- User registration with email and password.
- Token-based authenticationfor protected endpoints. 
- Create notification in multiple delivery channels.
- Strategy Pattern implementation for extensible notification delivery.
-  API documentation generated with Swagger

## Architecture
The application follows a layered architecture to promote separation of concerns and maintainability. The **Service** layer encapsulates all business logic, while the **Repository** layer is responsible for data access and database interactions. **Pydantic** models are used to validate and ensure the consistency of data throughout the application.

## Technologies
- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Docker & Docker Compose
- Pytest
- Uvicorn

## Project Strcuture
![alt text](image.png)

## Enviroment Variables
- **DATABASE_URL**: The database connection URL. This project uses SQLite by default.
- **SECRET_KEY**: A secret key used for authentication. It is recommended to use a randomly generated key with at least 48 characters.

## Prerequisites

The recommended way to run the application is with Docker.

### Using Docker

Make sure the following tools are installed:

- [Docker](https://docs.docker.com/get-docker/)
- Docker Compose, included with recent Docker Desktop installations


### Running Locally

To run the application without Docker, you need:

- Python 3.11 or later
- pip
- A Python virtual environment (recommended)

## Getting Started

Clone the repository:

```bash
git clone https://github.com/<your-username>/notifications-api.git
cd notifications-api
```

## Running with Docker


## Running Locally

## Running Tests

## API Documentation

## Adding a New Notification Channel

## Running Tests
