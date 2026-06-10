from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.assignments.router import router as assignments_router
from app.auth.router import router as auth_router
from app.dashboard.router import router as dashboard_router
from app.rule_engine.router import router as rule_engine_router
from app.tasks.router import router as tasks_router
from app.users.router import router as users_router

app = FastAPI(title="Task Management System")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(tasks_router)
app.include_router(rule_engine_router)
app.include_router(assignments_router)
app.include_router(users_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Task Management System API is running"}