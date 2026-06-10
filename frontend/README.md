# Task Management System - Frontend

## Overview

This is the React frontend for the Task Management System. It provides a modern web interface for managing tasks, defining eligibility rules, and viewing eligible users and tasks based on business rules.

The frontend communicates with the FastAPI backend using JWT-based authentication and REST APIs.

---

## Technology Stack

* React 19
* TypeScript
* Vite
* Material UI (MUI)
* Axios
* React Router DOM

---

## Features

### Authentication

* User Login
* JWT Token Management
* Protected Routes
* Automatic Authorization Header Injection

### Dashboard

* Total Tasks
* Total Rules
* Eligible Assignments Statistics

### Task Management

* Create New Tasks
* Set Priority
* Set Status
* Task Validation

### Rule Management

* Create Eligibility Rules
* Department Based Rules
* Experience Based Rules
* Location Based Rules
* Active Task Constraints

### Eligibility Engine

* Compute Eligible Users
* View Eligible Users
* View Eligible Tasks

---

## Project Structure

```text
src/
│
├── api/
│   └── api.ts
│
├── components/
│
├── context/
│   └── AuthContext.tsx
│
├── layouts/
│   └── MainLayout.tsx
│
├── pages/
│   ├── DashboardPage.tsx
│   ├── LoginPage.tsx
│   ├── CreateTaskPage.tsx
│   ├── CreateRulePage.tsx
│   ├── EligibleUsersPage.tsx
│   └── EligibleTasksPage.tsx
│
├── App.tsx
└── main.tsx
```

---

## Prerequisites

Install:

* Node.js 20+
* npm 10+

Verify installation:

```bash
node -v
npm -v
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd frontend
```

Install dependencies:

```bash
npm install
```

---

## Environment Configuration

Create a `.env` file in the frontend root:

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

## Running the Application

Start the development server:

```bash
npm run dev
```

Application URL:

```text
http://localhost:5173
```

---

## Backend Requirement

Ensure the FastAPI backend is running:

```bash
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

## Available Screens

### Login

Authenticate using registered user credentials.

### Dashboard

Displays:

* Total Tasks
* Total Rules
* Eligible Assignments

### Create Task

Create new tasks with:

* Title
* Description
* Priority
* Status

### Create Rule

Create task eligibility rules using:

* Department
* Experience
* Location
* Active Task Limits

### Eligible Users

Compute and view eligible users for a task.

### Eligible Tasks

View tasks available for a specific user.

---

## Authentication

JWT tokens are stored in browser local storage.

All protected API requests automatically include:

```http
Authorization: Bearer <token>
```

---

## Build for Production

Create production build:

```bash
npm run build
```

Preview production build:

```bash
npm run preview
```

---

## API Integration

Primary backend endpoints used:

```text
POST /auth/login
POST /auth/register

POST /tasks

POST /task-rules

POST /tasks/{task_id}/compute-eligibility

GET /tasks/{task_id}/eligible-users

GET /users/{user_id}/eligible-tasks

GET /dashboard/stats
```

---

## Future Enhancements

* Task List View
* Task Edit/Delete
* User Management
* Role Based Access Control
* Audit Logging
* Dark Mode
* Pagination
* Search & Filtering

---

## Author

Mayank Saxena

QA Architect | Mobile Testing Specialist | AI-Driven Quality Engineering
