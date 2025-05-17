try:
    from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
    from sqlalchemy.orm import Session, joinedload
    from sqlalchemy import func
    from . import models, schemas, crud
    from .database import engine, SessionLocal, Base
    import os, io, csv
    from uuid import uuid4
    from typing import Optional, List
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse
    from datetime import datetime
except Exception as e:
    import sys
    print(f"IMPORT ERROR: {e}", file=sys.stderr)
    raise



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

@app.get("/penguins/")
def get_all_penguins(sort_by: Optional[str] = None, db: Session = Depends(get_db)):
    penguins = crud.get_all_penguins_sorted(db, sort_by)

    # Subquery to get latest log date per penguin
    subquery = (
        db.query(
            models.MoultingLog.penguin_id.label("pid"),
            func.max(models.MoultingLog.date).label("last_seen")
        )
        .group_by(models.MoultingLog.penguin_id)
        .subquery()
    )

    # Build a lookup of penguin_id → last_seen
    last_seen_lookup = {
        row.pid: row.last_seen for row in db.query(subquery).all()
    }

    return [
        {
            "id": p.id,
            "name": p.name,
            "status": p.status,
            "mass": p.mass,
            "danger_flag": p.danger_flag,
            "last_seen": last_seen_lookup.get(p.id, "Never logged"),
            "images": [img.image_path for img in p.images]
        }
        for p in penguins
    ]

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

@app.get("/penguins/search")
def search_penguins(query: str, db: Session = Depends(get_db)):
    penguins = crud.search_penguins(db, query)

    # Get last_seen info
    subquery = (
        db.query(
            models.MoultingLog.penguin_id.label("pid"),
            func.max(models.MoultingLog.date).label("last_seen")
        )
        .group_by(models.MoultingLog.penguin_id)
        .subquery()
    )
    last_seen_lookup = {
        row.pid: row.last_seen for row in db.query(subquery).all()
    }

    return [
        {
            "id": p.id,
            "name": p.name,
            "status": p.status,
            "mass": p.mass,
            "danger_flag": p.danger_flag,
            "last_seen": last_seen_lookup.get(p.id, p.created_at)
        }
        for p in penguins
    ]

@app.get("/penguins/download")
def download_penguins_csv(db: Session = Depends(get_db)):
    penguins = crud.get_all_penguins_sorted(db)  # Reuse existing function

    # Get last_seen
    subquery = (
        db.query(
            models.MoultingLog.penguin_id.label("pid"),
            func.max(models.MoultingLog.date).label("last_seen")
        )
        .group_by(models.MoultingLog.penguin_id)
        .subquery()
    )
    last_seen_lookup = {
        row.pid: row.last_seen for row in db.query(subquery).all()
    }

    # Create in-memory CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "name", "status", "mass", "danger_flag", "last_seen"])

    for p in penguins:
        writer.writerow([
            p.id,
            p.name,
            p.status,
            p.mass,
            p.danger_flag,
            last_seen_lookup.get(p.id, p.created_at)
        ])

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=penguins.csv"
    })

@app.post("/penguins/{penguin_id}/upload-image-log")
def upload_image_and_log(
    penguin_id: int,
    stage: str = Form(...),
    mass: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
    ):
    # Save image
    upload_dir = "static/images"
    os.makedirs(upload_dir, exist_ok=True)
    image_ext = os.path.splitext(image.filename)[-1]
    image_filename = f"{uuid4().hex}{image_ext}"
    image_path = os.path.join(upload_dir, image_filename)

    with open(image_path, "wb") as buffer:
        buffer.write(image.file.read())

    image_url = f"/static/images/{image_filename}"

    # Save image to PenguinImage table
    db_image = models.PenguinImage(penguin_id=penguin_id, image_path=image_url)
    db.add(db_image)

    # Create moulting log entry
    moulting_log = models.MoultingLog(
        penguin_id=penguin_id,
        stage=stage,
        mass=mass,
        image_url=image_url
    )
    db.add(moulting_log)

    # 🔁 Update Penguin summary info
    penguin = db.query(models.Penguin).filter(models.Penguin.id == penguin_id).first()
    if penguin:
        penguin.status = stage
        penguin.mass = mass
        penguin.last_seen = datetime.utcnow()

    db.commit()
    
    return {
        "message": "Image and moulting log uploaded successfully.",
        "penguin_id": penguin_id,
        "stage": stage,
        "mass": mass,
        "image_url": image_url
    }


@app.get("/penguins/{penguin_id}/weight-trend")
def get_weight_trend(penguin_id: int, db: Session = Depends(get_db)):
    logs = (
        db.query(models.MoultingLog)
        .filter(models.MoultingLog.penguin_id == penguin_id)
        .order_by(models.MoultingLog.date.asc())
        .all()
    )
    return [
    {"date": log.date, "mass": log.mass, "image_url": log.image_url}
    for log in logs if log.mass is not None
    ]

@app.get("/penguins/{penguin_id}/with-logs", response_model=schemas.PenguinOutWithLogs)
def get_penguin_with_logs(penguin_id: int, db: Session = Depends(get_db)):
    penguin = (
        db.query(models.Penguin)
        .options(joinedload(models.Penguin.logs))
        .filter(models.Penguin.id == penguin_id)
        .first()
    )
    if not penguin:
        raise HTTPException(status_code=404, detail="Penguin not found")
    return penguin


