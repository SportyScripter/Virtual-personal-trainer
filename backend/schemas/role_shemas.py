from pydantic import BaseModel


class RoleCreate(BaseModel):
    role_name: str
    description: str


class RoleDelete(BaseModel):
    role_name: str
