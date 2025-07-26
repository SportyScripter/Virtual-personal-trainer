from pydantic import BaseModel


class BodyPartCreate(BaseModel):
    body_part_name: str


class ResponseModelBodyPart(BaseModel):
    id: int
