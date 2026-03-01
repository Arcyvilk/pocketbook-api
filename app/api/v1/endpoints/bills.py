from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from app.utils import DATA_PATH

import json
import datetime

router = APIRouter()

DATA_PATH_BILLS = f"{DATA_PATH}/bills.json"  # "f" means formatted string literal


class Bill(BaseModel):
    bill_id: str
    owner_id: str
    amount: int
    currency: str
    description: str
    created_at: str


@router.get("/")
def bills() -> list[Bill]:
    with open(DATA_PATH_BILLS, "r") as file:
        data = json.load(file)
    return data


@router.get("/{bill_id}")
def bill(bill_id: str) -> Bill:
    with open(DATA_PATH_BILLS, "r") as file:
        data = json.load(file)

    matched = [bill for bill in data if bill["bill_id"] == bill_id]

    if matched:
        return matched[0]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
def bill_create(bill: Bill):
    bill.created_at = datetime.datetime.now()
    with open(DATA_PATH_BILLS, "r") as file:
        data = json.load(file)

    data.append(bill)

    with open(DATA_PATH_BILLS, "w") as file:
        json.dump(data, file, indent=2)


@router.put("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def bill_update():
    return


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def bill_delete(bill_id: str):
    with open(DATA_PATH_BILLS, "r") as file:
        data = json.load(file)

    filtered_data = [bill for bill in data if bill["bill_id"] != bill_id]

    if len(data) == len(filtered_data):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found"
        )

    with open(DATA_PATH_BILLS, "w") as file:
        json.dump(filtered_data, file, indent=2)
