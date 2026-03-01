from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/")
def index():
    return {"message": "I'm working!"}


@app.get("/users")
def users():
    with open("app/data/users.json", "r") as file:
        data = json.load(file)
    return data
