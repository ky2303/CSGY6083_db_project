from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, create_engine, Session
from typing import List
from pydantic import BaseModel
from models import INTEL_ITEMS, GROUPS, MITIGATIONS, TACTICS, TECHNIQUES, SOFTWARE, STANDARDS

sqlite_file_name = "intel_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

app = FastAPI()

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
        db_item=session.query(INTEL_ITEMS).filter(INTEL_ITEMS.id == item_id).first()
        db_item.name=item.name
        db_item.description=item.description
        db_item.url=item.url
        db_item.comments=item.comments
        db_item.date_added=item.date_added
        db_item.last_updated=item.last_updated
        db_item.GROUPS_id=item.GROUPS_id
        db_item.MITIGATIONS_id=item.MITIGATIONS_id
        db_item.TACTICS_id=item.TACTICS_id
        db_item.TECHNIQUES_id=item.TECHNIQUES_id
        db_item.SOFTWARE_id=item.SOFTWARE_id
        db_item.STANDARDS_id=item.STANDARDS_id
        db_item.image=item.image

        session.commit()
        return JSONResponse(content=db_item.dict())

@app.delete("/intel_items/{item_id}")
def delete_item(item_id:int):
    with Session(engine) as session:
        item=session.query(INTEL_ITEMS).filter(INTEL_ITEMS.id == item_id).first()
        session.delete(item)
        session.commit()