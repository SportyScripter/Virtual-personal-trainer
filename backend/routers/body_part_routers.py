from db.session import get_db
from schemas.body_part import BodyPartCreate
from sqlalchemy.orm import Session
from models.body_part import BodyPart
from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, status
from models.body_part import BodyPart

body_part_router = APIRouter(prefix="/body_parts", tags=["body_parts"])


class BodyPartEnum(Enum):
    CHEST = "Klatka piersiowa"
    BACK = "Plecy"
    THIGHS = "Uda"
    CALVES = "Łydki"
    BICEPS = "Biceps"
    TRICEPS = "Triceps"
    FOREARMS = "Przedramiona"
    SHOULDERS = "Barki"
    ABS = "Brzuch"
    GLUTES = "Pośladki"


def seed_body_parts(db: Session):
    for part in BodyPartEnum:
        exists = db.query(BodyPart).filter_by(body_part_name=part.value).first()
        if not exists:
            db.add(BodyPart(body_part_name=part.value))
            print(f"Added body part: {part.value}")
    db.commit()


@body_part_router.get("/list")
async def get_body_parts(db: Session = Depends(get_db)):
    body_parts = db.query(BodyPart.id, BodyPart.body_part_name).all()
    if not body_parts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No body parts found",
        )
    return [{"id": bp.id, "body_part_name": bp.body_part_name} for bp in body_parts]
