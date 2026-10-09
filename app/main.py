from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, expenses

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="User registration, JWT auth and per-user expense CRUD.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}
