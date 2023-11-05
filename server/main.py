from fastapi import APIRouter, FastAPI
from database import create_group_table, shutdown_db_connection, startup_db_connection
from routers import groups

app = FastAPI()

@app.on_event("startup")
async def startup():
    startup_db_connection()

@app.on_event("shutdown")
async def shutdown():
    shutdown_db_connection()

@app.on_event("startup")
async def init_tables():
    create_group_table()

app.include_router(groups.router, prefix="/groups", tags=["groups"])

# Create a root hello world GET endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

