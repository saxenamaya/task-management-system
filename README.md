# Task Management System

A full-stack Task Management System built using **FastAPI**, **React**, and **SQLite**, featuring JWT authentication, a configurable rule engine, automatic eligibility computation, and assignment management.

The system enables organizations to define task eligibility rules and automatically determine which users qualify for specific tasks based on configurable criteria.

---

# Features

## User Management

* User Registration
* User Login
* JWT-based Authentication
* Role Support

  * ADMIN
  * MANAGER
  * USER
* User Profile Updates
* Automatic Eligibility Recalculation on User Updates

---

## Task Management

* Create Tasks
* Update Tasks
* Delete Tasks
* Task Status Tracking
* Task Priority Management
* Due Date Support

---

## Rule Engine

Configure eligibility rules per task using:

* Department
* Minimum Experience
* Maximum Active Tasks
* Location

---

## Assignment Engine

* Compute Eligible Users
* Store Assignment Results
* View Eligible Users for a Task
* View Eligible Tasks for a User
* Automatic Assignment Recalculation

---

## Automatic Eligibility Recalculation

Eligibility is automatically recomputed when:

* A Rule is Created
* A Rule is Updated
* A User Profile is Updated

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

## Backend Setup

```bash
cd backend

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend URL:

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

| Method | Endpoint       | Description   |
| ------ | -------------- | ------------- |
| POST   | /auth/register | Register User |
| POST   | /auth/login    | Login User    |

---

## Users

| Method | Endpoint         | Description                                   |
| ------ | ---------------- | --------------------------------------------- |
| PUT    | /users/{user_id} | Update User Profile and Recompute Eligibility |

---

## Tasks

| Method | Endpoint         | Description |
| ------ | ---------------- | ----------- |
| POST   | /tasks           | Create Task |
| PUT    | /tasks/{task_id} | Update Task |
| DELETE | /tasks/{task_id} | Delete Task |

---

## Task Rules

| Method | Endpoint              | Description |
| ------ | --------------------- | ----------- |
| POST   | /task-rules           | Create Rule |
| PUT    | /task-rules/{task_id} | Update Rule |

---

## Assignments

| Method | Endpoint                             | Description            |
| ------ | ------------------------------------ | ---------------------- |
| POST   | /tasks/{task_id}/compute-eligibility | Compute Eligible Users |
| GET    | /tasks/{task_id}/eligible-users      | Get Eligible Users     |
| GET    | /users/{user_id}/eligible-tasks      | Get Eligible Tasks     |

---

## Dashboard

| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | /dashboard/stats | Dashboard Statistics |

---

# Authentication

## Login Response

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

### Frontend

JWT token is stored in:

```text
localStorage["token"]
```

Axios automatically adds:

```http
Authorization: Bearer <token>
```

to authenticated requests.

### Backend

Uses:

* OAuth2 Password Bearer
* JWT Validation
* Current User Resolution via Dependency Injection

---

# Sample Workflow

1. Register a User
2. Login and Receive JWT Token
3. Create a Task
4. Create a Rule
5. Eligible Users are Automatically Computed
6. Update Users or Rules
7. Assignments Automatically Refresh
8. View Eligible Users
9. View Eligible Tasks
10. Review Dashboard Statistics

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

* Least-Loaded User Assignment
* Round-Robin Assignment
* Priority-Based Assignment
* Workload Balancing Algorithms

---

# Frontend Screens

| Screen         | Purpose                         |
| -------------- | ------------------------------- |
| Login          | Authentication                  |
| Dashboard      | Metrics and Overview            |
| Create Task    | Create Tasks                    |
| Create Rule    | Create Eligibility Rules        |
| Eligible Users | Compute and View Eligible Users |
| Eligible Tasks | View Eligible Tasks for a User  |

---

# Development Environment Considerations

This solution was developed and validated in a corporate-managed environment with restrictions on installing containerization and infrastructure tooling.

As a result:

* Docker Desktop was not available for installation.
* Redis services could not be provisioned locally.
* Background worker frameworks such as Celery/RQ were not configured.
* SQLite was used for local development and demonstration purposes.

The application architecture has been intentionally designed using a layered Router → Service → Repository pattern, enabling straightforward future integration of:

* PostgreSQL
* Redis Caching
* Celery/RQ Background Processing
* Docker-Based Deployment
* Kubernetes Orchestration

The current implementation focuses on delivering the complete functional requirements while documenting the scalability roadmap for production deployment.

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

* PostgreSQL Migration
* Redis Caching
* Background Workers (Celery/RQ)
* Role-Based Authorization (RBAC)
* User Management UI
* Audit Logging
* Email/Slack Notifications
* Search and Filtering
* Pagination
* Docker Deployment
* Kubernetes Deployment
* Least-Loaded User Assignment Strategy
* Round-Robin Assignment Strategy

---

# Documentation

* Backend README
* Frontend README
* Architecture Documentation

---

# Author

**Mayank Saxena**
