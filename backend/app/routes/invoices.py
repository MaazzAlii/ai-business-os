from fastapi import APIRouter
from app.db.database import run_query

router = APIRouter()


@router.get("/")
def list_all_invoices():
    """Return all invoices joined with vendor name."""
    return run_query("""
        SELECT  i.id,
                i.invoice_number,
                v.name          AS vendor_name,
                i.total_amount,
                i.currency,
                i.invoice_date,
                i.due_date,
                i.status,
                i.created_at
        FROM    invoices i
        JOIN    vendors  v ON v.id = i.vendor_id
        ORDER   BY i.created_at DESC
    """)


@router.get("/unpaid")
def list_unpaid_invoices():
    """Return only unpaid and overdue invoices."""
    return run_query("""
        SELECT  i.invoice_number,
                v.name          AS vendor,
                i.total_amount,
                i.due_date,
                i.status,
                (i.due_date < CURRENT_DATE) AS is_overdue
        FROM    invoices i
        JOIN    vendors  v ON v.id = i.vendor_id
        WHERE   i.status IN ('unpaid', 'overdue')
        ORDER   BY i.due_date ASC
    """)


@router.get("/summary")
def invoice_summary():
    """Return total amounts grouped by status."""
    return run_query("""
        SELECT  status,
                COUNT(*)            AS count,
                SUM(total_amount)   AS total
        FROM    invoices
        GROUP   BY status
        ORDER   BY total DESC
    """)


@router.get("/{invoice_id}")
def get_single_invoice(invoice_id: str):
    """Return one invoice with all its line items."""
    invoice = run_query(
        "SELECT * FROM invoices WHERE id = :id",
        {"id": invoice_id}
    )
    if not invoice:
        return {"error": "Invoice not found"}

    items = run_query(
        "SELECT * FROM invoice_items WHERE invoice_id = :id",
        {"id": invoice_id}
    )
    result = invoice[0]
    result["line_items"] = items
    return result
