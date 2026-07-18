from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so Alembic can discover them
from app.db.models.rule_template import RuleTemplate

