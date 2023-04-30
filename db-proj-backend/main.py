from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlmodel import create_engine, Session
from typing import List
from models import INTEL_ITEMS, GROUPS, MITIGATIONS, TACTICS, TECHNIQUES, SOFTWARE, STANDARDS
from fastapi.middleware.cors import CORSMiddleware

sqlite_file_name = "intel_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

app = FastAPI(
    title="db_project",
    description="""
    # 🔍 Threat Intelligence Tracking Database

    ## github
    https://github.com/ky2303/CSGY6083_db_project

    ## frontent (WIP)
    http://localhost:3000/

    ## FastAPI
    https://fastapi.tiangolo.com/

    """
)

origins = [
    "http://localhost:3000",
    "http://34.172.159.141:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
def read_items(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        items = session.query(INTEL_ITEMS).offset(skip).limit(limit).all()
        return items


@app.get("/intel_items/{item_id}", response_model=INTEL_ITEMS)
def read_item(item_id: int):
    with Session(engine) as session:
        item = session.query(INTEL_ITEMS).filter(
            INTEL_ITEMS.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Intel item not found")
        return item


@app.put("/intel_items/{item_id}")
def update_item(item_id: int, item: INTEL_ITEMS):
    with Session(engine) as session:
        db_item = session.query(INTEL_ITEMS).filter(
            INTEL_ITEMS.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Intel item not found")
        db_item.name = item.name
        db_item.description = item.description
        db_item.url = item.url
        db_item.comments = item.comments
        db_item.date_added = item.date_added
        db_item.last_updated = item.last_updated
        db_item.GROUPS_id = item.GROUPS_id
        db_item.MITIGATIONS_id = item.MITIGATIONS_id
        db_item.TACTICS_id = item.TACTICS_id
        db_item.TECHNIQUES_id = item.TECHNIQUES_id
        db_item.SOFTWARE_id = item.SOFTWARE_id
        db_item.STANDARDS_id = item.STANDARDS_id
        db_item.image = item.image

        session.commit()
        session.refresh(db_item)
        return JSONResponse(content=db_item.dict())


@app.delete("/intel_items/{item_id}")
def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.query(INTEL_ITEMS).filter(
            INTEL_ITEMS.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Intel item not found")
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
def read_groups(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        groups = session.query(GROUPS).offset(skip).all()
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
        db_group.id = group.id
        db_group.name = group.name
        db_group.url = group.url
        db_group.associated_groups = group.associated_groups
        db_group.description = group.description
        db_group.techniques_used = group.techniques_used
        db_group.techniques_used_ids = group.techniques_used_ids
        db_group.software = group.software
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


#MITIGATIONS


@app.post("/mitigations/", response_model=MITIGATIONS)
def create_mitigation(mitigation: MITIGATIONS):
    with Session(engine) as session:
        # need to check if id is already in use
        db_mitigation = MITIGATIONS.from_orm(mitigation)
        session.add(db_mitigation)
        session.commit()
        session.refresh(db_mitigation)
        return db_mitigation


@app.get("/mitigations/", response_model=List[MITIGATIONS])
def read_mitigations(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        mitigations = session.query(MITIGATIONS).offset(skip).all()
        return mitigations


@app.get("/mitigations/{mitigation_id}", response_model=MITIGATIONS)
def read_mitigation(mitigation_id: int):
    with Session(engine) as session:
        mitigation = session.query(MITIGATIONS).filter(MITIGATIONS.id == mitigation_id).first()
        if not mitigation:
            raise HTTPException(status_code=404, detail="Mitigation not found")
        return mitigation


@app.put("/mitigations/{mitigation_id}", response_model=MITIGATIONS)
def update_mitigation(mitigation_id: int, mitigation: MITIGATIONS):
    with Session(engine) as session:
        db_mitigation = session.query(MITIGATIONS).filter(MITIGATIONS.id == mitigation_id).first()
        if not db_mitigation:
            raise HTTPException(status_code=404, detail="Mitigation not found")
        db_mitigation.id = mitigation.id
        db_mitigation.name = mitigation.name
        db_mitigation.description = mitigation.description
        db_mitigation.url = mitigation.url
        db_mitigation.policy_or_control = mitigation.policy_or_control
        db_mitigation.related_framework = mitigation.related_framework
        db_mitigation.TECHNIQUES_id = mitigation.TECHNIQUES_id
        db_mitigation.STANDARDS_id = mitigation.software
        session.add(db_mitigation)
        session.commit()
        session.refresh(db_mitigation)
        return db_mitigation


@app.delete("/mitigations/{mitigation_id}")
def delete_mitigation(mitigation_id: int):
    with Session(engine) as session:
        db_mitigation = session.query(MITIGATIONS).filter(MITIGATIONS.id == mitigation_id).first()
        if not db_mitigation:
            raise HTTPException(status_code=404, detail="Mitigation not found")
        session.delete(db_mitigation)
        session.commit()

#TACTICS


@app.post("/tactics/")
def create_tactic(tactic: TACTICS):
    with Session(engine) as session:
        session.add(tactic)
        session.commit()
        session.refresh(tactic)
        return tactic

@app.get("/tactics/", response_model=List[TACTICS])
def read_tactics():
    with Session(engine) as session:
        tactics = session.query(TACTICS).all()
        return tactics

@app.get("/tactics/{tactic_id}", response_model=TACTICS)
def read_tactic(tactic_id: int):
    with Session(engine) as session:
        tactic = session.get(TACTICS, tactic_id)
        if not tactic:
            raise HTTPException(status_code=404, detail="Tactic not found")
        return tactic

@app.put("/tactics/{tactic_id}")
def update_tactic(tactic_id: int, tactic: TACTICS):
    with Session(engine) as session:
        db_tactic = session.get(TACTICS, tactic_id)
        if not db_tactic:
            raise HTTPException(status_code=404, detail="Tactic not found")
        tactic_data = tactic.dict(exclude_unset=True)
        for key, value in tactic_data.items():
            setattr(db_tactic, key, value)
        session.add(db_tactic)
        session.commit()
        session.refresh(db_tactic)
        return db_tactic

@app.delete("/tactics/{tactic_id}")
def delete_tactic(tactic_id: int):
    with Session(engine) as session:
        tactic = session.get(TACTICS, tactic_id)
        if not tactic:
            raise HTTPException(status_code=404, detail="Tactic not found")
        session.delete(tactic)
        session.commit()


#TECHNIQUES


@app.post("/techniques/")
def create_technique(technique: TECHNIQUES):
    with Session(engine) as session:
        session.add(technique)
        session.commit()
        session.refresh(technique)
        return technique

@app.get("/techniques/", response_model=List[TECHNIQUES])
def read_techniques():
    with Session(engine) as session:
        techniques = session.query(TECHNIQUES).all()
        return techniques

@app.get("/techniques/{technique_id}", response_model=TECHNIQUES)
def read_technique(technique_id: int):
    with Session(engine) as session:
        technique = session.get(TECHNIQUES, technique_id)
        if not technique:
            raise HTTPException(status_code=404, detail="Technique not found")
        return technique

@app.put("/techniques/{technique_id}")
def update_technique(technique_id: int, technique: TECHNIQUES):
    with Session(engine) as session:
        db_technique = session.get(TECHNIQUES, technique_id)
        if not db_technique:
            raise HTTPException(status_code=404, detail="Technique not found")
        technique_data = technique.dict(exclude_unset=True)
        for key, value in technique_data.items():
            setattr(db_technique, key, value)
        session.add(db_technique)
        session.commit()
        session.refresh(db_technique)
        return db_technique

@app.delete("/techniques/{technique_id}")
def delete_technique(technique_id: int):
    with Session(engine) as session:
        technique = session.get(TECHNIQUES, technique_id)
        if not technique:
            raise HTTPException(status_code=404, detail="Technique not found")
        session.delete(technique)
        session.commit()


#SOFTWARE


@app.post("/software/")
def create_software(software: SOFTWARE):
    with Session(engine) as session:
        session.add(software)
        session.commit()
        session.refresh(software)
        return software

@app.get("/software/", response_model=List[SOFTWARE])
def read_software():
    with Session(engine) as session:
        software = session.query(SOFTWARE).all()
        return software

@app.get("/software/{software_id}", response_model=SOFTWARE)
def read_software(software_id: int):
    with Session(engine) as session:
        software = session.get(SOFTWARE, software_id)
        if not software:
            raise HTTPException(status_code=404, detail="Software not found")
        return software

@app.put("/software/{software_id}")
def update_software(software_id: int, software: SOFTWARE):
    with Session(engine) as session:
        db_software = session.get(SOFTWARE, software_id)
        if not db_software:
            raise HTTPException(status_code=404, detail="Software not found")
        software_data = software.dict(exclude_unset=True)
        for key, value in software_data.items():
            setattr(db_software, key, value)
        session.add(db_software)
        session.commit()
        session.refresh(db_software)
        return db_software

@app.delete("/software/{software_id}")
def delete_software(software_id: int):
    with Session(engine) as session:
        software = session.get(SOFTWARE, software_id)
        if not software:
            raise HTTPException(status_code=404, detail="Software not found")
        session.delete(software)
        session.commit()


#STANDARDS


@app.post("/standards/")
def create_standard(standard: STANDARDS):
    with Session(engine) as session:
        session.add(standard)
        session.commit()
        session.refresh(standard)
        return standard

@app.get("/standards/", response_model=List[STANDARDS])
def read_standards():
    with Session(engine) as session:
        standards = session.query(STANDARDS).all()
        return standards

@app.get("/standards/{standard_id}", response_model=STANDARDS)
def read_standard(standard_id: int):
    with Session(engine) as session:
        standard = session.get(STANDARDS, standard_id)
        if not standard:
            raise HTTPException(status_code=404, detail="Standard not found")
        return standard

@app.put("/standards/{standard_id}")
def update_standard(standard_id: int, standard: STANDARDS):
    with Session(engine) as session:
        db_standard = session.get(STANDARDS, standard_id)
        if not db_standard:
            raise HTTPException(status_code=404, detail="Standard not found")
        standard_data = standard.dict(exclude_unset=True)
        for key, value in standard_data.items():
            setattr(db_standard, key, value)
        session.add(db_standard)
        session.commit()
        session.refresh(db_standard)
        return db_standard

@app.delete("/standards/{standard_id}")
def delete_standard(standard_id: int):
    with Session(engine) as session:
        standard = session.get(STANDARDS, standard_id)
        if not standard:
            raise HTTPException(status_code=404, detail="Standard not found")
        session.delete(standard)
        session.commit()

# REPORT

@app.get("/report/top_groups")
async def top_groups(lim: int = Query(..., description="The number of top groups to return")):
    with Session(engine) as session:
        # Query the INTEL_ITEMS table for the top "lim" occurrences of the "group" column
        top_groups = session.execute(
            "SELECT GROUPS_id, (SELECT name FROM GROUPS WHERE id = INTEL_ITEMS.GROUPS_id) as group_name, COUNT(*) as count FROM INTEL_ITEMS GROUP BY GROUPS_id ORDER BY count DESC LIMIT :lim",
            {"lim": lim}
        ).fetchall()
        print(top_groups)

        # Create a dictionary mapping group names to their occurrences
        result = {}
        for group in top_groups:
            result[group[0]] = [ group[1] , group[2] ]

    return JSONResponse(result)