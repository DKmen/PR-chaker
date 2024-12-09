from fastapi import FastAPI
from app.api.v1.endpoints import analyze
from app.api.v1.endpoints import status
from app.api.v1.endpoints import result
from app.db.session import create_db_and_tables


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(analyze.router, prefix="/analyze-pr", tags=["analyze"])
app.include_router(status.router, prefix="/status", tags=["status"])
app.include_router(result.router, prefix="/result", tags=["result"])
