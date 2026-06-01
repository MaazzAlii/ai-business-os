# AI Business OS Backend

## Setup

1. Copy the example environment file:

```powershell
copy .env.example .env
```

2. Update `.env` with PostgreSQL credentials and your Mistral API key.

3. Install dependencies:

If you're on Windows and see build errors when installing (native wheels need C/C++ or Rust), follow one of the options below.

### Option A — Windows (MSVC) + Rust toolchain

Install Visual C++ Build Tools and Rust, then install packages inside the venv:

```powershell
# Install Visual C++ Build Tools (run as admin)
winget install --id Microsoft.VisualStudio.2022.BuildTools -e

# Install Rust (rustup)
iwr -useb https://win.rustup.rs | iex
rustup default stable

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Option B — Conda (recommended on Windows)

```powershell
conda create -n ai-business-os python=3.11 -y
conda activate ai-business-os
conda install -c conda-forge fastapi uvicorn pydantic sqlalchemy psycopg2-binary python-dotenv httpx python-multipart pdfplumber -y
```

### Option C — Docker (build inside Linux container)

```powershell
cd backend
docker build -t ai-business-os-backend .
docker run --rm -p 8000:8000 --name ai-business-os-backend ai-business-os-backend
```

If you used Option A or B, verify installation with:

```powershell
pip show fastapi
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
