from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.task_repository import TaskRepository
from app.repositories.task_rule_repository import TaskRuleRepository
from app.rule_engine.models import TaskRule
from app.rule_engine.schemas import TaskRuleCreate, TaskRuleResponse, TaskRuleUpdate
from app.services.assignment_service import AssignmentService

router = APIRouter(tags=["task-rules"])


@router.post(
    "/task-rules",
    response_model=TaskRuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_rule(
    payload: TaskRuleCreate,
    db: Session = Depends(get_db),
) -> TaskRule:
    task_repository = TaskRepository(db)
    task_rule_repository = TaskRuleRepository(db)

    task = task_repository.get_task_by_id(payload.task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {payload.task_id} not found",
        )

    if task_rule_repository.get_rule_by_task_id(payload.task_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Task with id {payload.task_id} already has a rule",
        )

    rule = TaskRule(
        task_id=payload.task_id,
        department=payload.department,
        min_experience=payload.min_experience,
        max_active_tasks=payload.max_active_tasks,
        location=payload.location,
    )

    created_rule = task_rule_repository.create_rule(rule)

    db.commit()

    # -----------------------------------------
    # AUTO COMPUTE ELIGIBILITY
    # -----------------------------------------
    assignment_service = AssignmentService(db)
    assignment_service.compute_eligibility(payload.task_id)

    return created_rule

@router.put(
    "/task-rules/{task_id}",
    response_model=TaskRuleResponse,
)
def update_task_rule(
    task_id: int,
    payload: TaskRuleUpdate,
    db: Session = Depends(get_db),
) -> TaskRule:
    task_rule_repository = TaskRuleRepository(db)

    rule = task_rule_repository.get_rule_by_task_id(task_id)

    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No rule found for task {task_id}",
        )

    rule.department = payload.department
    rule.min_experience = payload.min_experience
    rule.max_active_tasks = payload.max_active_tasks
    rule.location = payload.location

    updated_rule = task_rule_repository.update_rule(rule)

    db.commit()

    # ---------------------------------
    # AUTO RECOMPUTE ELIGIBILITY
    # ---------------------------------
    assignment_service = AssignmentService(db)
    assignment_service.compute_eligibility(task_id)

    return updated_rule