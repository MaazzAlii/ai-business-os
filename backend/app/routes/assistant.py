from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.database import run_query
from app.services.mistral_service import ask_mistral
from datetime import date

router = APIRouter()


# ── Request model ──────────────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str


# ── SQL helper functions ───────────────────────────────────────────────────
# Each function runs one specific SQL query and returns the result.
# The build_context() function below calls these based on the question.

def get_unpaid_invoices() -> list:
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

def get_monthly_summary(year: int, month: int) -> dict:
    rows = run_query("""
        SELECT
            COUNT(*)                                        AS total_invoices,
            COALESCE(SUM(total_amount), 0)                  AS total_amount,
            COALESCE(SUM(CASE WHEN status='paid'
                         THEN total_amount END), 0)         AS paid_amount,
            COALESCE(SUM(CASE WHEN status='unpaid'
                         THEN total_amount END), 0)         AS unpaid_amount
        FROM invoices
        WHERE EXTRACT(YEAR  FROM invoice_date) = :year
          AND EXTRACT(MONTH FROM invoice_date) = :month
    """, {"year": year, "month": month})
    return rows[0] if rows else {}

def get_vendor_summary() -> list:
    return run_query("""
        SELECT  v.name                  AS vendor,
                COUNT(i.id)             AS total_invoices,
                SUM(i.total_amount)     AS total_spent
        FROM    vendors  v
        JOIN    invoices i ON i.vendor_id = v.id
        GROUP   BY v.name
        ORDER   BY total_spent DESC
    """)

def get_expense_by_category() -> list:
    return run_query("""
        SELECT  ii.category,
                COUNT(*)                AS line_items,
                SUM(ii.total_price)     AS total
        FROM    invoice_items ii
        GROUP   BY ii.category
        ORDER   BY total DESC
    """)


# ── System prompt for Mistral ──────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an AI business assistant for a small business in Pakistan.
You have access to the business's real financial data shown below.
Answer the user's question clearly, accurately, and concisely.
Use PKR for all currency amounts. Format with commas: PKR 45,000
If the data shows nothing relevant, say so honestly.
Never invent numbers that are not in the data.
Keep answers under 200 words unless a list requires more.
"""


# ── Context builder ────────────────────────────────────────────────────────
def build_context(question: str) -> str:
    """
    This function decides WHICH data to pull from the database
    based on keywords found in the user's question.
    
    This is called 'intent-based context routing' — the same
    pattern used in production RAG systems.
    """
    q = question.lower()
    context_parts = []

    # Always include unpaid invoices — most business questions involve money owed
    unpaid = get_unpaid_invoices()
    if unpaid:
        context_parts.append(f"UNPAID AND OVERDUE INVOICES:\n{unpaid}")

    # Monthly summary if question is about sales, revenue, or a time period
    if any(word in q for word in ["month", "last month", "this month", "sell", "sold", "revenue", "total"]):
        today = date.today()
        summary = get_monthly_summary(today.year, today.month)
        context_parts.append(f"THIS MONTH SUMMARY:\n{summary}")

    # Vendor info if question is about suppliers
    if any(word in q for word in ["supplier", "vendor", "who", "most", "biggest", "history"]):
        vendors = get_vendor_summary()
        context_parts.append(f"VENDOR SUMMARY:\n{vendors}")

    # Expense categories if question is about spending
    if any(word in q for word in ["expense", "category", "spend", "spent", "cost"]):
        cats = get_expense_by_category()
        context_parts.append(f"EXPENSES BY CATEGORY:\n{cats}")

    if context_parts:
        return "\n\n".join(context_parts)
    else:
        return "No matching data found in the database."


# ── API endpoint ───────────────────────────────────────────────────────────
@router.post("/ask")
def ask_business_question(req: QuestionRequest):
    """
    Main endpoint: receives a question, builds database context,
    sends to Mistral AI, returns the answer.
    
    Called by: n8n Workflow 0 and the Streamlit frontend
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Step 1: Pull relevant data from PostgreSQL
        context = build_context(req.question)

        # Step 2: Combine context + question into a single message
        full_message = f"Business data:\n{context}\n\nUser question: {req.question}"

        # Step 3: Ask Mistral
        answer = ask_mistral(SYSTEM_PROMPT, full_message)

        return {
            "question":     req.question,
            "answer":       answer,
            "context_used": context[:400] + "..." if len(context) > 400 else context
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.mistral_service import ask_mistral_question

router = APIRouter(tags=["assistant"])


class AssistantRequest(BaseModel):
    question: str


class AssistantResponse(BaseModel):
    answer: str


@router.post("/assistant", response_model=AssistantResponse)
async def ask_assistant(payload: AssistantRequest) -> AssistantResponse:
    try:
        answer = await ask_mistral_question(payload.question)
        return AssistantResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
