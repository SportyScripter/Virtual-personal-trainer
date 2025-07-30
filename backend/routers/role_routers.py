from fastapi import APIRouter, Depends, HTTPException, status
from db.session import get_db
from sqlalchemy.orm import Session
from schemas.role_shemas import RoleCreate, RoleDelete
from models.role import Role
from enum import Enum


class role(Enum):
    User = "Użytkownik"
    Trainer = "Trener"


def seed_roles(db: Session):
    for role_name in role:
        exists = db.query(Role).filter_by(role_name=role_name.name).first()
        if not exists:
            db.add(Role(role_name=role_name.name, description=role_name.value))
            print(f"Added role: {role_name.name}")
    db.commit()


role_routers = APIRouter(prefix="/role", tags=["role"])


@role_routers.post("/create", response_model=RoleCreate)
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
):
    db_role = db.query(Role).filter(Role.role_name == role.role_name).first()
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists",
        )
    new_role = Role(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@role_routers.delete("/delete/{role_id}", response_model=RoleDelete)
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    db.delete(db_role)
    db.commit()
    return {"detail": "Role deleted successfully"}
