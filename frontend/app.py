import streamlit as st
import requests
import pandas as pd

# ── Config ─────────────────────────────────────────────────────────────────
API_BASE  = "http://localhost:8000/api"
N8N_HOOK  = "http://localhost:5678/webhook/business-question"

st.set_page_config(
    page_title="AI Business OS",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Business OS")
st.caption("Powered by n8n + FastAPI + Mistral AI")

# ── Tabs ───────────────────────────────────────────────────────────────────
tab_assistant, tab_invoices = st.tabs(["🤖 AI Assistant", "📄 Invoices"])


# ── Tab 1: AI Assistant ────────────────────────────────────────────────────
with tab_assistant:
    st.subheader("Ask your business a question")

    # Quick question buttons
    st.write("**Quick questions:**")
    col1, col2, col3, col4 = st.columns(4)
    quick_q = None
    if col1.button("Unpaid invoices"):   quick_q = "Which invoices are unpaid?"
    if col2.button("Biggest supplier"):  quick_q = "Who is my biggest supplier?"
    if col3.button("Monthly expenses"):  quick_q = "What are my total expenses this month?"
    if col4.button("Overdue invoices"):  quick_q = "Show me overdue invoices"

    st.write("")
    question = st.text_input(
        "Or type your own question:",
        value=quick_q if quick_q else "",
        placeholder="e.g. What did I spend on supplies?"
    )

    if st.button("Ask AI", type="primary") and question:
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    N8N_HOOK,
                    json={"question": question},
                    timeout=30
                )
                if resp.ok:
                    data = resp.json()
                    st.success("**Answer:**")
                    st.write(data.get("answer", "No answer returned"))
                    with st.expander("See data used"):
                        st.write(data.get("context_used", ""))
                else:
                    st.error(f"Error {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"Could not reach n8n or FastAPI: {e}")


# ── Tab 2: Invoices ────────────────────────────────────────────────────────
with tab_invoices:
    st.subheader("Invoice records")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if st.button("Load all invoices"):
            try:
                resp = requests.get(f"{API_BASE}/invoices/", timeout=10)
                if resp.ok:
                    df = pd.DataFrame(resp.json())
                    st.dataframe(
                        df[["invoice_number", "vendor_name", "total_amount", "due_date", "status"]],
                        use_container_width=True
                    )
            except Exception as e:
                st.error(str(e))

    with col_b:
        if st.button("Unpaid only"):
            try:
                resp = requests.get(f"{API_BASE}/invoices/unpaid", timeout=10)
                if resp.ok:
                    df = pd.DataFrame(resp.json())
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(str(e))

    with col_c:
        if st.button("Summary by status"):
            try:
                resp = requests.get(f"{API_BASE}/invoices/summary", timeout=10)
                if resp.ok:
                    df = pd.DataFrame(resp.json())
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(str(e))
