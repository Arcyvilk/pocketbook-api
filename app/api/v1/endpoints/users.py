from fastapi import APIRouter
from pydantic import BaseModel
from app.utils import DATA_PATH

import json


router = APIRouter()

DATA_PATH_USERS = f"{DATA_PATH}/users.json"  # "f" means formatted string literal


class User(BaseModel):
    user_id: str
    name: str


@router.get("/")
def users():
    with open(DATA_PATH_USERS, "r") as file:
        data = json.load(file)
    return data


@router.get("/{user_id}")
def user(user_id: str):
    with open(DATA_PATH_USERS, "r") as file:
        data = json.load(file)

    matched = [user for user in data if user["user_id"] == user_id]

    if matched:
        return matched[0]
    return {"error": "User not found"}
