from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
import json
import datetime

router = APIRouter()

API_PATH = "app/_data"


############################################################
#                                                          #
#                     USERS ENDPOINTS                      #
#                                                          #
############################################################

API_PATH_USERS = f"{API_PATH}/users.json"  # "f" means formatted string literal


class User(BaseModel):
    user_id: str
    name: str


@router.get("/users", tags=["users"])
def users():
    with open(API_PATH_USERS, "r") as file:
        data = json.load(file)
    return data


@router.get("/users/{user_id}", tags=["users"])
def user(user_id: str):
    with open(API_PATH_USERS, "r") as file:
        data = json.load(file)
    for user in data:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}


############################################################
#                                                          #
#                     BILLS ENDPOINTS                      #
#                                                          #
############################################################

API_PATH_BILLS = f"{API_PATH}/bills.json"  # "f" means formatted string literal


class Bill(BaseModel):
    bill_id: str
    owner_id: str
    amount: int
    currency: str
    created_at: str


@router.get("/bills", tags=["bills"])
def bills() -> list[Bill]:
    with open(API_PATH_BILLS, "r") as file:
        data = json.load(file)
    return data


@router.get("/bills/{bill_id}", tags=["bills"])
def bill(bill_id: str) -> Bill:
    with open(API_PATH_BILLS, "r") as file:
        data = json.load(file)
    for bill in data:
        if bill["bill_id"] == bill_id:
            return bill

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")


@router.post("/bills", tags=["bills"], status_code=status.HTTP_201_CREATED)
def bill_create(bill: Bill):
    bill.created_at = datetime.datetime.now()
    with open(API_PATH_BILLS, "r") as file:
        data = json.load(file)
    data.append(bill)
    with open(API_PATH_BILLS, "w") as file:
        json.dump(data, file, indent=2)


@router.put("/bills/{bill_id}", tags=["bills"], status_code=status.HTTP_204_NO_CONTENT)
def bill_update():
    return


@router.delete(
    "/bills/{bill_id}", tags=["bills"], status_code=status.HTTP_204_NO_CONTENT
)
def bill_delete(bill_id: str):
    with open(API_PATH_BILLS, "r") as file:
        data = json.load(file)
    for bill in data:
        if bill["bill_id"] == bill_id:
            data.remove(bill)
            with open(API_PATH_BILLS, "w") as file:
                json.dump(data, file, indent=2)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")
