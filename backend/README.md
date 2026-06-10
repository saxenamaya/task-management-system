# Task Management System

A FastAPI-based Task Management System that assigns tasks to eligible users using a configurable rule engine.

---

## Features

### User Management
- User registration
- User authentication using JWT
- Role support (ADMIN, MANAGER, USER)

### Task Management
- Create tasks
- Track status
- Track priority
- Due date support

### Rule Engine
Define eligibility rules for tasks:

- Department
- Minimum experience
- Maximum active tasks
- Location

### Assignment Engine
Automatically computes eligible users for a task and stores assignment results.

### Security
- JWT Authentication
- OAuth2 Password Flow
- Protected APIs

---

## Architecture

FastAPI follows a layered architecture:

```
Router Layer
     ↓
Service Layer
     ↓
Repository Layer
     ↓
SQLite Database
```

### Components

#### Routers
Expose REST APIs.

#### Services
Business logic.

#### Repositories
Database access.

#### Models
SQLAlchemy entities.

#### Schemas
Pydantic request/response models.

---

## Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- JWT
- Passlib (bcrypt)
- Pydantic

---

## Project Structure

app/

├── auth/

├── users/

├── tasks/

├── rule_engine/

├── assignments/

├── repositories/

├── services/

├── db/

└── core/

---

## Database Entities

### User

| Field | Description |
|---------|---------|
| id | User ID |
| name | User name |
| email | Unique email |
| password_hash | Encrypted password |
| role | ADMIN / MANAGER / USER |
| department | User department |
| experience_years | Experience |
| location | User location |
| active_task_count | Current workload |

### Task

| Field | Description |
|---------|---------|
| id | Task ID |
| title | Task title |
| description | Task details |
| status | TODO / IN_PROGRESS / DONE |
| priority | LOW / MEDIUM / HIGH |

### TaskRule

Eligibility rules for tasks.

### TaskAssignment

Stores computed eligibility results.

---

## API Endpoints

### Authentication

POST /auth/register

POST /auth/login

### Tasks

POST /tasks

### Task Rules

POST /task-rules

### Assignments

POST /tasks/{task_id}/compute-eligibility

GET /tasks/{task_id}/eligible-users

GET /users/{user_id}/eligible-tasks

---

## Authentication Flow

### Register

POST /auth/register

### Login

POST /auth/login

Returns:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

### Swagger Authorization

1. Login
2. Click Authorize
3. Enter username and password
4. Swagger automatically attaches JWT token

---

## Running the Application

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
alembic upgrade head
```

### Start Application

```bash
uvicorn app.main:app --reload
```

### Swagger

http://127.0.0.1:8000/docs

---

## Sample Workflow

1. Register user
2. Login
3. Create task
4. Create task rule
5. Compute eligibility
6. View eligible users
7. View eligible tasks

---

## Future Enhancements

- PostgreSQL support
- Role-based authorization
- Task update APIs
- Task deletion APIs
- Audit logging
- Notification service
- Docker deployment
- Kubernetes deployment

---

## Author

Mayank Saxena
