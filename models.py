from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint
from typing import Optional

class INTEL_ITEMS(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    url: Optional[str] = None
    comments: Optional[str] = None
    date_added: Optional[str] = None
    last_updated: Optional[str] = None
    GROUPS_id: Optional[int] = None
    MITIGATIONS_id: Optional[int] = None
    TACTICS_id: Optional[int] = None
    TECHNIQUES_id: Optional[int] = None
    SOFTWARE_id: Optional[int] = None
    STANDARDS_id: Optional[int] = None
    image: Optional[bytes] = None


class GROUPS(SQLModel, table=True):
    __table_args__=(UniqueConstraint("name"),)
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    url: str = Field(nullable=False)
    associated_groups: Optional[str] = None
    description: Optional[str] = None
    techniques_used: Optional[str] = None
    techniques_used_ids: Optional[str] = None
    software: Optional[str] = None

class MITIGATIONS(SQLModel, table=True):
    __table_args__=(UniqueConstraint("name"),)
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    url: Optional[str] = None
    policy_or_control: int = None
    related_framework: Optional[str] = None
    TECHNIQUES_id: Optional[int] = None
    STANDARDS_id: Optional[int] = None

class TACTICS(SQLModel, table=True):
    __table_args__=(UniqueConstraint("name"),)
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    url: Optional[str] = None

class TECHNIQUES(SQLModel, table=True):
    __table_args__=(UniqueConstraint("name"),)
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    url: Optional[str] = None
    associated_tactic: Optional[str] = None
    TACTICS_id: Optional[int] = None
    is_child: int = None
    parent_id: Optional[int] = None
    mitigation_control: Optional[str] = None
    mitigation_policy: Optional[str] = None

class SOFTWARE(SQLModel, table=True):
    __table_args__=(UniqueConstraint("name"),)
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    url: Optional[str] = None
    related_framework: Optional[str] = None
    TECHNIQUES_id: Optional[int] = None

class STANDARDS(SQLModel, table=True):
    __table_args__=(UniqueConstraint("name"),)
    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    regulatory_body: Optional[str] = None
    url: Optional[str] = None