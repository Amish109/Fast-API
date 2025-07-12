from fastapi import FastAPI
from . import models, database
from dotenv import load_dotenv
load_dotenv()  # Load variables from .env file

from .routers import company , employee
models.Base.metadata.create_all(bind=database.engine)
# Create all the tables in the database, based on the models you've defined using Base

app = FastAPI()
app.include_router(company.router)  
app.include_router(employee.router)  

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with SQLAlchemy!"}



# To Run server 
# uvicorn app.main:app --reload
# app.main means:
# app → folder
# main.py → file
# app → FastAPI instance in that file