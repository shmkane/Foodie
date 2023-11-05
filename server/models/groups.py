from pydantic import BaseModel


class Group(BaseModel):
    id: str
    name: str
    dishes: list
    restrictions: list
