from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlmodel import  create_engine, Session
from typing import List
from models import INTEL_ITEMS, GROUPS, MITIGATIONS, TACTICS, TECHNIQUES, SOFTWARE, STANDARDS

sqlite_file_name = "intel_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

app = FastAPI(
    title="db_project",
    description="""
    Threat Intelligence Tracking Database

    ## github
    https://github.com/ky2303/CSGY6083_db_project
    """
)

# INTEL_ITEMS
@app.post("/intel_items/")
def create_item(item: INTEL_ITEMS):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return JSONResponse(content=item.dict())

@app.get("/intel_items/", response_model=List[INTEL_ITEMS])
def read_items(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        items = session.query(INTEL_ITEMS).offset(skip).limit(limit).all()
        return items

@app.get("/intel_items/{item_id}", response_model=INTEL_ITEMS)
def read_item(item_id: int):
    with Session(engine) as session:
        item = session.query(INTEL_ITEMS).filter(INTEL_ITEMS.id == item_id).first()
        return item

@app.put("/intel_items/{item_id}")
def update_item(item_id:int, item: INTEL_ITEMS):
    with Session(engine) as session:
        db_item = session.query(INTEL_ITEMS).filter(INTEL_ITEMS.id == item_id).first()
        db_item.name            = item.name
        db_item.description     = item.description
        db_item.url             = item.url
        db_item.comments        = item.comments
        db_item.date_added      = item.date_added
        db_item.last_updated    = item.last_updated
        db_item.GROUPS_id       = item.GROUPS_id
        db_item.MITIGATIONS_id  = item.MITIGATIONS_id
        db_item.TACTICS_id      = item.TACTICS_id
        db_item.TECHNIQUES_id   = item.TECHNIQUES_id
        db_item.SOFTWARE_id     = item.SOFTWARE_id
        db_item.STANDARDS_id    = item.STANDARDS_id
        db_item.image           = item.image

        session.commit()
        session.refresh(db_item)
        return JSONResponse(content=db_item.dict())

@app.delete("/intel_items/{item_id}")
def delete_item(item_id:int):
    with Session(engine) as session:
        item=session.query(INTEL_ITEMS).filter(INTEL_ITEMS.id == item_id).first()
        session.delete(item)
        session.commit()

# GROUPS
@app.post("/groups/", response_model=GROUPS)
def create_group(group: GROUPS):
    with Session(engine) as session:
        # need to check if id is already in use
        db_group = GROUPS.from_orm(group)
        session.add(db_group)
        session.commit()
        session.refresh(db_group)
        return db_group 

@app.get("/groups/", response_model=List[GROUPS])
def read_groups(skip: int = 0, limit: int = 100):
    with Session(engine) as session:
        groups = session.query(GROUPS).offset(skip).limit(limit).all()
        return groups

@app.get("/groups/{group_id}", response_model=GROUPS)
def read_group(group_id: int):
    with Session(engine) as session:
        group = session.query(GROUPS).filter(GROUPS.id == group_id).first()
        return group

@app.put("/groups/{group_id}", response_model=GROUPS)
def update_group(group_id: int, group: GROUPS):
    with Session(engine) as session:
        db_group = session.query(GROUPS).filter(GROUPS.id == group_id).first()
        db_group.id                  = group.id
        db_group.name                = group.name
        db_group.url                 = group.url
        db_group.associated_groups   = group.associated_groups
        db_group.description         = group.description
        db_group.techniques_used     = group.techniques_used
        db_group.techniques_used_ids = group.techniques_used_ids
        db_group.software            = group.software
        session.add(db_group)
        session.commit()
        session.refresh(db_group)
        return db_group

@app.delete("/groups/{group_id}")
def delete_group(group_id: int):
    with Session(engine) as session:
        db_group = session.query(GROUPS).filter(GROUPS.id == group_id).first()
        session.delete(db_group)
        session.commit()