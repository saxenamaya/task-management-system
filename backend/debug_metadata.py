from app.db.database import Base
from app.users.models import User
from app.tasks.models import Task
from app.rule_engine.models import TaskRule

print(Base.metadata.tables.keys())