# Task Management System

A full-stack Task Management System built using **FastAPI**, **React**, and **SQLite**, featuring JWT authentication, a configurable rule engine, automatic eligibility computation, and assignment management.

The system enables organizations to define task eligibility rules and automatically determine which users qualify for specific tasks based on configurable criteria.

---

# Features

## User Management

* User registration
* User login
* JWT-based authentication
* Role support:

  * ADMIN
  * MANAGER
  * USER
* User profile updates
* Automatic eligibility recomputation on user updates

---

## Task Management

* Create tasks
* Update tasks
* Delete tasks
* Task status tracking
* Task priorities
* Due date support

---

## Rule Engine

Configure eligibility rules per task:

* Department
* Minimum experience
* Maximum active tasks
* Location

---

## Assignment Engine

* Compute eligible users
* Store assignment results
* View eligible users for a task
* View eligible tasks for a user
* Automatic assignment recomputation

---

## Automatic Eligibility Recalculation

Eligibility is automatically recomputed when:

* A rule is created
* A rule is updated
* A user profile is updated

This ensures assignment results remain synchronized with rule changes.

---

## Dashboard

Real-time dashboard metrics:

* Total Tasks
* Total Rules
* Eligible Assignments

---

# Architecture

```text
                 ┌───────────────┐
                 │  React (MUI)  │
                 └───────┬───────┘
                         │ REST + JWT
                         ▼
                 ┌───────────────┐
                 │    FastAPI    │
                 └───────┬───────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   Auth Router      Task Router    Assignment Router
        │                │                │
        └────────┬───────┴───────┬────────┘
                 ▼               ▼
             Services       Rule Engine
                 │
                 ▼
            Repositories
                 │
                 ▼
              SQLite
```

Backend follows a layered architecture:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

---

# Technology Stack

| Layer          | Technologies                                      |
| -------------- | ------------------------------------------------- |
| Backend        | Python 3.13, FastAPI, SQLAlchemy, Alembic, SQLite |
| Authentication | JWT, OAuth2, Passlib (bcrypt)                     |
| Frontend       | React 19, TypeScript, Vite                        |
| UI             | Material UI                                       |
| API Client     | Axios                                             |
| Routing        | React Router DOM                                  |

---

# Project Structure

```text
task-management-system/
│
├── backend/
│   ├── app/
│   │   ├── auth/
│   │   ├── users/
│   │   ├── tasks/
│   │   ├── rule_engine/
│   │   ├── assignments/
│   │   ├── dashboard/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── db/
│   │   └── core/
│   │
│   ├── alembic/
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── context/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   └── README.md
│
├── docs/
│
└── README.md
```

---

# Prerequisites

## Backend

* Python 3.13+
* pip

## Frontend

* Node.js 20+
* npm 10+

---

# Quick Start

## Backend

```bash
cd backend

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```text
http://localhost:5173
```

Optional:

Create:

```text
frontend/.env
```

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

# API Endpoints

## Authentication

| Method | Endpoint         | Description   |
| ------ | ---------------- | ------------- |
| POST   | `/auth/register` | Register user |
| POST   | `/auth/login`    | Login user    |

---

## Users

| Method | Endpoint           | Description                                   |
| ------ | ------------------ | --------------------------------------------- |
| PUT    | `/users/{user_id}` | Update user profile and recompute eligibility |

---

## Tasks

| Method | Endpoint           | Description |
| ------ | ------------------ | ----------- |
| POST   | `/tasks`           | Create task |
| PUT    | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

---

## Task Rules

| Method | Endpoint                | Description |
| ------ | ----------------------- | ----------- |
| POST   | `/task-rules`           | Create rule |
| PUT    | `/task-rules/{task_id}` | Update rule |

---

## Assignments

| Method | Endpoint                               | Description            |
| ------ | -------------------------------------- | ---------------------- |
| POST   | `/tasks/{task_id}/compute-eligibility` | Compute eligible users |
| GET    | `/tasks/{task_id}/eligible-users`      | Get eligible users     |
| GET    | `/users/{user_id}/eligible-tasks`      | Get eligible tasks     |

---

## Dashboard

| Method | Endpoint           | Description          |
| ------ | ------------------ | -------------------- |
| GET    | `/dashboard/stats` | Dashboard statistics |

---

# Authentication

## Login Response

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

## Frontend

JWT token is stored in:

```text
localStorage["token"]
```

Axios automatically adds:

```http
Authorization: Bearer <token>
```

to authenticated requests.

## Backend

Uses:

* OAuth2 Password Bearer
* JWT validation
* Current user resolution via dependency injection

---

# Sample Workflow

1. Register a user
2. Login and receive JWT token
3. Create a task
4. Create a rule
5. Eligible users are automatically computed
6. Update users or rules
7. Assignments automatically refresh
8. View eligible users
9. View eligible tasks
10. Review dashboard statistics

---

# Database Entities

## User

| Field             | Description            |
| ----------------- | ---------------------- |
| id                | User ID                |
| name              | User Name              |
| email             | Unique Email           |
| password_hash     | Hashed Password        |
| role              | ADMIN / MANAGER / USER |
| department        | Department             |
| experience_years  | Experience             |
| location          | User Location          |
| active_task_count | Current Workload       |

---

## Task

| Field       | Description               |
| ----------- | ------------------------- |
| id          | Task ID                   |
| title       | Task Title                |
| description | Task Details              |
| status      | TODO / IN_PROGRESS / DONE |
| priority    | LOW / MEDIUM / HIGH       |
| due_date    | Due Date                  |

---

## TaskRule

Stores eligibility criteria for a task.

---

## TaskAssignment

Stores computed eligibility results.

---

# Assignment Strategy

Current implementation stores all eligible users for a task.

Potential future enhancements:

* Least-loaded user assignment
* Round-robin assignment
* Priority-based assignment
* Workload balancing algorithms

---

# Frontend Screens

| Screen         | Purpose                         |
| -------------- | ------------------------------- |
| Login          | Authentication                  |
| Dashboard      | Metrics and overview            |
| Create Task    | Create tasks                    |
| Create Rule    | Create eligibility rules        |
| Eligible Users | Compute and view eligible users |
| Eligible Tasks | View eligible tasks for a user  |

---

# Build for Production

## Backend

Run using a production ASGI server such as:

```bash
gunicorn -k uvicorn.workers.UvicornWorker
```

## Frontend

```bash
cd frontend

npm run build

npm run preview
```

---

# Future Enhancements

* PostgreSQL migration
* Redis caching
* Background workers (Celery/RQ)
* Role-based authorization
* User management UI
* Audit logging
* Notifications
* Search and filtering
* Pagination
* Docker deployment
* Kubernetes deployment

---

# Documentation

* Backend README
* Frontend README
* Architecture Documentation

---

# Author

**Mayank Saxena**
