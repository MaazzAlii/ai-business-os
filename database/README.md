# Database Setup for AI Business OS

## Local PostgreSQL with Docker

Start a PostgreSQL container:

```powershell
docker run -d --name biz-os-db -p 5432:5432 \
  -e POSTGRES_USER=bizadmin \
  -e POSTGRES_PASSWORD=SuperSecureP@ssw0rd \
  -e POSTGRES_DB=ai_business_os \
  postgres:15
```

Create the database schema:

```powershell
docker exec -it biz-os-db psql -U bizadmin -d ai_business_os -f /schema.sql
```

If you want to keep the schema file outside the container, copy it first:

```powershell
docker cp database/schema.sql biz-os-db:/schema.sql
```

## Environment

Copy `backend/.env.example` to `backend/.env` and update secrets as needed.

## Run the backend

```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Notes

- The backend uses SQLAlchemy and will also create the `invoices` table automatically on startup when `backend/app/main.py` runs.
- The `MISTRAL_API_KEY` environment variable is required for the assistant route to call the Mistral API.
