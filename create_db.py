from sqlmodel import SQLModel, create_engine, Field
from sqlalchemy import UniqueConstraint
from typing import Optional
from models import INTEL_ITEMS, GROUPS, MITIGATIONS, TACTICS, TECHNIQUES, SOFTWARE, STANDARDS

sqlite_file_name = "intel_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

INTEL_ITEMS.__table__.create(engine)
GROUPS.__table__.create(engine)
MITIGATIONS.__table__.create(engine)
TACTICS.__table__.create(engine)
TECHNIQUES.__table__.create(engine)
SOFTWARE.__table__.create(engine)
STANDARDS.__table__.create(engine)
