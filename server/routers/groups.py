from fastapi import APIRouter, HTTPException
from database import get_database
from models.groups import Group
import json



router = APIRouter()
database = get_database()

@router.get("/{group_id}", response_model=Group)
async def get_group(group_id: int):
    query = "SELECT * FROM groups WHERE id = :group_id"
    group = await database.fetch_one(query=query, values={"group_id": group_id})

    return group

@router.get("/", response_model=list[Group])
async def get_all_groups():
    query = "SELECT * FROM groups"
    groups = await database.fetch_all(query)

    return groups

@router.post("/", response_model=Group)
async def create_group(group: Group):
    query = 'INSERT INTO groups (name, dishes, restrictions) VALUES (:name, :dishes, :restrictions) RETURNING id, name, dishes, restrictions'
    values = {
        "name": group.name,
        "dishes": json.dumps(group.dishes),
        "restrictions": json.dumps(group.restrictions)
    }

    created_group = await database.fetch_one(query=query, values=values)

    created_group["dishes"] = json.loads(created_group["dishes"])
    created_group["restrictions"] = json.loads(created_group["restrictions"])

    return created_group


@router.patch("/{group_id}", response_model=Group)
async def patch_group(group_id: int, updated_group: Group):
    query = "SELECT * FROM groups WHERE id = :group_id"
    existing_group = await database.fetch_one(query, {"group_id": group_id})

    if existing_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    # Merge the updates with the existing group data
    updated_data = updated_group.dict(exclude_unset=True)
    updated_data["id"] = group_id

    # Update the group in the database
    update_query = "UPDATE groups SET name = :name, dishes = :dishes, restrictions = :restrictions WHERE id = :id RETURNING *"
    updated_group = await database.fetch_one(update_query, values=updated_data)

    return updated_group


@router.delete("/groups/{group_id}", response_model=Group)
async def delete_group(group_id: int):
    # Check if the group exists
    query = "SELECT * FROM groups WHERE id = :group_id"
    existing_group = await database.fetch_one(query, {"group_id": group_id})

    if existing_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    # Delete the group from the database
    delete_query = "DELETE FROM groups WHERE id = :group_id RETURNING *"
    deleted_group = await database.fetch_one(delete_query, {"group_id": group_id})

    return deleted_group