from pydantic import BaseModel
from typing import Optional


class GroupCreate(BaseModel):
    name: str
    dishes: Optional[list[str]] = []
    restrictions: Optional[list[str]] = []

class GroupGetDelete(BaseModel):
    id: str
    name: str
    dishes: Optional[list[str]] 
    restrictions: Optional[list[str]] 

class Group(GroupCreate):
    id: str
