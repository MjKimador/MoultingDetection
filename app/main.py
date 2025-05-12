from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base
from typing import List
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/penguins/", response_model=schemas.PenguinOut)
def create_penguin(penguin: schemas.PenguinCreate, db: Session = Depends(get_db)):
    return crud.create_penguin(db, penguin)

@app.get("/penguins/", response_model=List[schemas.PenguinOut])
def read_penguins(db: Session = Depends(get_db)):
    return crud.get_penguins(db)
@app.post("/logs/", response_model=schemas.MoultingLogOut)
def add_log(log: schemas.MoultingLogCreate, db: Session = Depends(get_db)):
    penguin = crud.get_penguin(db, log.penguin_id)
    if not penguin:
        raise HTTPException(status_code=404, detail="Penguin not found")
    return crud.create_moulting_log(db, log)

@app.get("/penguins/{penguin_id}/logs", response_model=List[schemas.MoultingLogOut])
def get_logs(penguin_id: int, db: Session = Depends(get_db)):
    penguin = db.query(models.Penguin).filter(models.Penguin.id == penguin_id).first()
    if not penguin:
        raise HTTPException(status_code=404, detail="Penguin not found")

    logs = db.query(models.MoultingLog).filter(models.MoultingLog.penguin_id == penguin_id).order_by(models.MoultingLog.date.desc()).all()
    return logs

@app.get("/analytics/at-risk", response_model=List[schemas.PenguinOut])
def get_risk_penguins(db: Session = Depends(get_db)):
    return crud.get_risk_penguins(db)
@app.get("/analytics/stats")
def stage_stats(db: Session = Depends(get_db)):
    return crud.get_stage_counts(db)

@app.get("/analytics/colony-stats")
def colony_stats(db: Session = Depends(get_db)):
    return crud.get_colony_stats(db)

@app.get("/analytics/unlogged")
def unlogged_penguins(db: Session = Depends(get_db)):
    data = crud.get_unlogged_penguins(db)
    return [
        {
            "id": penguin.id,
            "name": penguin.name,
            "status": penguin.status,
            "mass": penguin.mass,
            "danger_flag": penguin.danger_flag,
            "last_seen": log_date.isoformat() if log_date else "Never logged"
        }
        for penguin, log_date in data
    ]
@app.delete("/penguins/{penguin_id}")
def delete_penguin(penguin_id: int, db: Session = Depends(get_db)):
    result = crud.delete_penguin(db, penguin_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Penguin not found")
    return {"message": f"Penguin {penguin_id} deleted successfully."}

