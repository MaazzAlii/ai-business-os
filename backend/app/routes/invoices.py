from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.models.invoice import Invoice

router = APIRouter(prefix="/invoices", tags=["invoices"])


class InvoiceCreate(BaseModel):
    customer_name: str = Field(..., example="Acme Corp")
    total_amount: float = Field(..., example=199.99)
    status: str = Field(default="pending", example="pending")
    due_date: date | None = Field(default=None, example="2025-01-31")


class InvoiceResponse(BaseModel):
    id: int
    customer_name: str
    total_amount: float
    status: str
    due_date: date | None
    created_at: datetime

    class Config:
        orm_mode = True


@router.post("/", response_model=InvoiceResponse)
async def create_invoice(
    invoice: InvoiceCreate,
    session: Session = Depends(get_session),
) -> InvoiceResponse:
    invoice_record = Invoice(
        customer_name=invoice.customer_name,
        total_amount=invoice.total_amount,
        status=invoice.status,
        due_date=invoice.due_date,
    )
    session.add(invoice_record)
    session.commit()
    session.refresh(invoice_record)
    return invoice_record


@router.get("/", response_model=list[InvoiceResponse])
async def list_invoices(session: Session = Depends(get_session)) -> list[InvoiceResponse]:
    invoices = session.scalars(select(Invoice)).all()
    return invoices


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    session: Session = Depends(get_session),
) -> InvoiceResponse:
    invoice_record = session.get(Invoice, invoice_id)
    if not invoice_record:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice_record
