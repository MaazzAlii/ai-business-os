from fastapi import FastAPI

from app.db.database import init_db
from app.routes.assistant import router as assistant_router
from app.routes.invoices import router as invoices_router

app = FastAPI(title="AI Business OS", version="0.1.0")
app.include_router(assistant_router)
app.include_router(invoices_router)


@app.on_event("startup")
async def on_startup() -> None:
    init_db()


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "AI Business OS API Running"}
