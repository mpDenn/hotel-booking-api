# Hotel Booking API

A REST API for hotel room booking built with FastAPI and PostgreSQL.

The project includes user authentication, role-based access control, room management, booking validation, conflict detection, database migrations, automated tests, and Docker support.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic
- JWT authentication
- Pytest
- Docker
- Docker Compose

## Features

- User registration and authentication
- JWT-based authorization
- Role-based access control for users and admins
- Room creation, retrieval, and price updates
- Booking creation, retrieval, update, and deletion
- Booking conflict detection
- Guest capacity validation
- Validation for invalid and past booking dates
- Users can access and manage only their own bookings
- Admin endpoints for user and room management
- PostgreSQL database with SQLAlchemy ORM
- Database migrations with Alembic
- Automated API tests with Pytest
- Docker and Docker Compose support

## API Endpoints

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/users` | Register a new user | Public |
| POST | `/login` | Authenticate user and receive JWT token | Public |
| GET | `/me` | Get current user profile | Authenticated |
| GET | `/users` | Get all users | Admin |
| GET | `/user/{user_id}` | Get user by ID | Admin |
| PATCH | `/user/{user_id}` | Update user | Admin |
| DELETE | `/user/{user_id}` | Delete user | Admin |
| GET | `/rooms` | Get all rooms | Public |
| GET | `/rooms/{room_id}` | Get room by ID | Public |
| POST | `/rooms` | Create a room | Admin |
| PATCH | `/rooms/{room_id}` | Update room price | Admin |
| POST | `/booking` | Create a booking | Authenticated |
| GET | `/booking/me` | Get current user's bookings | Authenticated |
| PATCH | `/booking/{booking_id}` | Update booking dates | Owner |
| DELETE | `/booking/{booking_id}` | Delete booking | Owner |

## Running the Project

### Docker

Create a `.env.docker` file in the project root:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=hotel_booking

DATABASE_URL=postgresql://postgres:your_password@db:5432/hotel_booking
SECRET_KEY=replace_with_a_secure_secret_key
```

Build and start the containers:

```bash
docker compose up --build -d
```

Apply database migrations:

```bash
docker compose exec api alembic upgrade head
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Local Development

Make sure PostgreSQL is running locally.

Install the dependencies:

```bash
py -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/hotel_booking
SECRET_KEY=replace_with_a_secure_secret_key
```

Apply database migrations:

```bash
py -m alembic upgrade head
```

Start the API:

```bash
py -m uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Testing

Run the test suite with:

```bash
py -m pytest
```

The tests cover authentication, booking creation, validation, booking conflicts, authorization, and deletion behavior.

## Project Structure

```text
hotel-booking-api/
├── alembic/              # Database migrations
├── models/               # SQLAlchemy database models
│   ├── booking.py
│   ├── rooms.py
│   └── user.py
├── routers/              # FastAPI endpoints
│   ├── auth.py
│   ├── booking.py
│   ├── room.py
│   └── user.py
├── schemas/              # Pydantic request/response schemas
│   ├── auth.py
│   ├── booking.py
│   ├── rooms.py
│   └── user.py
├── services/             # Business logic and authentication
│   ├── booking.py
│   ├── rooms.py
│   ├── security.py
│   └── user.py
├── tests/                # Automated API tests and fixtures
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_basic.py
│   └── test_booking.py
├── database.py           # Database configuration
├── main.py               # FastAPI application entry point
├── Dockerfile
├── compose.yaml
├── alembic.ini
└── requirements.txt
```

## Authentication

The API uses JWT Bearer authentication.

After logging in through `/login`, the client receives an access token that must be included in protected requests:

```http
Authorization: Bearer <access_token>
```

Access tokens expire after 30 minutes.

Admin-only endpoints additionally require the authenticated user to have the `admin` role.