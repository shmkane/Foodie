from pydantic import BaseModel


class Dish(BaseModel):
    name: str
    ingredients: list
