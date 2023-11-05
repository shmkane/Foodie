from fastapi import APIRouter, HTTPException
from database import get_database
from models.groups import Group, GroupCreate, GroupGetDelete
from uuid import uuid4
import json


router = APIRouter()
database = get_database()

@router.get("/get/{group_id}", response_model=Group)
async def get_group(group_id: int):
    query = "SELECT * FROM groups WHERE id = :group_id"
    group = await database.fetch_one(query=query, values={"group_id": group_id})

    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    return dict(group)

@router.get("/list", response_model=list[GroupGetDelete])
async def get_all_groups():
    query = "SELECT * FROM groups"
    groups = await database.fetch_all(query)

    # Convert the list of tuples into a list of dictionaries
    group_list = []
    for group_tuple in groups:
        group_dict = {
            "id": group_tuple[0],
            "name": group_tuple[1],
            "dishes": json.loads(group_tuple[2]),
            "restrictions": json.loads(group_tuple[3])
        }
        group_list.append(group_dict)

    return group_list

@router.post("/create", response_model=Group)
async def create_group(group: GroupCreate):
    query = 'INSERT INTO groups (id, name, dishes, restrictions) VALUES (:id, :name, :dishes, :restrictions) RETURNING id, name, dishes, restrictions'
    values = {
        "id": str(uuid4()), 
        "name": group.name,
        "dishes": json.dumps(group.dishes) ,
        "restrictions": json.dumps(group.restrictions)
    }

    created_group = await database.fetch_one(query=query, values=values)

    print(created_group)

    if created_group is None:
        raise HTTPException(status_code=500, detail="Could not create group")

    created_group_dict = dict(created_group)
    print(created_group_dict)

    created_group_dict["dishes"] = json.loads(created_group_dict["dishes"])
    created_group_dict["restrictions"] = json.loads(created_group_dict["restrictions"])

    return created_group_dict


@router.patch("/update/{group_id}", response_model=Group)
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

    updated_group_dict = dict(updated_group)

    return updated_group_dict


@router.delete("/delete/{group_id}", response_model=GroupGetDelete)
async def delete_group(group_id: int):
    query = "SELECT * FROM groups WHERE id = :group_id"
    existing_group = await database.fetch_one(query, {"group_id": group_id})

    if existing_group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    delete_query = "DELETE FROM groups WHERE id = :group_id RETURNING *"
    deleted_group = await database.fetch_one(delete_query, {"group_id": group_id})

    deleted_group_dict = dict(deleted_group)

    return deleted_group_dict


@router.delete("/delete_all")
async def delete_all_groups():
    query = "DELETE FROM groups"
    response = await database.execute(query)
    print(response)

# n groups deleted
    return {"message": f"{response} groups deleted"}