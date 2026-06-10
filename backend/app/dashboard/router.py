from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.assignments.models import TaskAssignment
from app.db.database import get_db
from app.rule_engine.models import TaskRule
from app.tasks.models import Task

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
):
    task_count = db.query(func.count(Task.id)).scalar()

    rule_count = db.query(func.count(TaskRule.id)).scalar()

    eligible_user_count = (
        db.query(func.count(TaskAssignment.id))
        .filter(TaskAssignment.is_eligible.is_(True))
        .scalar()
    )

    return {
        "tasks": task_count,
        "rules": rule_count,
        "eligible_users": eligible_user_count,
    }
