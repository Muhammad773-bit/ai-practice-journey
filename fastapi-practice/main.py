from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/greet")
def greet():
    return {"greeting": "Hello, FastAPI user!"}

@app.get('/greet/{name}')
def greet_name(name: str, age: Optional[int] = None):
    if age is not None:
        return {"greeting": f"Hello, {name}! You are {age} years old."}