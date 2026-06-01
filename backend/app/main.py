from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import invoices, assistant

app = FastAPI(
    title="AI Business OS",
    description="Business automation backend - Phase 1",
    version="0.1.0"
)

# This allows your Streamlit frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the route files you will create in Steps 7 and 8
app.include_router(invoices.router,  prefix="/api/invoices",  tags=["invoices"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["assistant"])

@app.get("/")
def health_check():
    return {"status": "ok", "service": "AI Business OS"}
