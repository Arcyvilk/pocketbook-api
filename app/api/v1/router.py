from fastapi import APIRouter
import json

router = APIRouter()


# USER ENDPOINTS
@router.get("/users")
def users():
    with open("app/_data/users.json", "r") as file:
        data = json.load(file)
    return data
