import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routes import boards, columns, tasks

load_dotenv()

# Create tables if they do not already exist (schema.sql documents the design;
# this keeps a fresh clone runnable without a manual migration step).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # Pydantic validation errors (e.g. empty title) surface as 400s with a
    # simple message the frontend can display directly. exc.errors() can
    # contain non-JSON-serializable objects (e.g. the raised ValueError
    # instance in "ctx"), so we extract just the message strings.
    messages = [error.get("msg", "Invalid input") for error in exc.errors()]
    return JSONResponse(status_code=400, content={"detail": messages})


app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(tasks.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
