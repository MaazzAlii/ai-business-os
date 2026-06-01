import streamlit as st
import httpx

BACKEND_URL = st.secrets.get("backend_url", "http://localhost:8000")

st.set_page_config(page_title="AI Business OS", page_icon="🚀")
st.title("AI Business OS")
st.write("Ask the assistant a business question and manage invoices from a simple UI.")

question = st.text_area("Ask the assistant", height=120)
if st.button("Send question"):
    if not question.strip():
        st.warning("Enter a question before sending.")
    else:
        with st.spinner("Querying the assistant..."):
            try:
                response = httpx.post(
                    f"{BACKEND_URL}/assistant",
                    json={"question": question},
                    timeout=30,
                )
                response.raise_for_status()
                answer = response.json().get("answer", "No answer returned.")
                st.success(answer)
            except Exception as exc:
                st.error(f"Assistant request failed: {exc}")

st.divider()
st.subheader("Invoice sample")
with st.expander("Create sample invoice"):
    customer_name = st.text_input("Customer name", value="Acme Corp")
    amount = st.number_input("Total amount", min_value=0.0, value=199.99)
    status = st.selectbox("Status", ["pending", "paid", "overdue"])
    due_date = st.date_input("Due date")

    if st.button("Create invoice"):
        with st.spinner("Saving invoice..."):
            try:
                response = httpx.post(
                    f"{BACKEND_URL}/invoices",
                    json={
                        "customer_name": customer_name,
                        "total_amount": float(amount),
                        "status": status,
                        "due_date": due_date.isoformat(),
                    },
                    timeout=30,
                )
                response.raise_for_status()
                invoice = response.json()
                st.success("Invoice created")
                st.json(invoice)
            except Exception as exc:
                st.error(f"Invoice creation failed: {exc}")
