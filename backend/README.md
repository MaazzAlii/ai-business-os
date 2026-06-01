# AI Business OS Backend

## Setup

1. Copy the example environment file:

```powershell
copy .env.example .env
```

2. Update `.env` with PostgreSQL credentials and your Mistral API key.

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API endpoints

- `GET /` - health check
- `POST /assistant` - ask the AI assistant a question
- `POST /invoices` - create a new invoice
- `GET /invoices` - list invoices
- `GET /invoices/{invoice_id}` - retrieve one invoice
