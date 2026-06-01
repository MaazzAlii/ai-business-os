docker exec -it biz-os-db psql -U bizadmin -d ai_business_os -f /schema.sql
docker cp database/schema.sql biz-os-db:/schema.sql
# Database Setup for AI Business OS

## Local PostgreSQL with Docker

Make sure Docker Desktop is running, then start PostgreSQL:

```powershell
docker run --name biz-os-db \
  -e POSTGRES_USER=bizadmin \
  -e POSTGRES_PASSWORD=bizpass123 \
  -e POSTGRES_DB=ai_business_os \
  -p 5432:5432 \
  -d postgres:15
```

Verify the container started:

```powershell
docker ps
# You should see: biz-os-db ... Up X seconds
```

### Create the tables (inside the container)

Copy the schema file into the container (if not already present):

```powershell
docker cp database/schema.sql biz-os-db:/schema.sql
```

Connect to the database and run the SQL:

```powershell
docker exec -it biz-os-db psql -U bizadmin -d ai_business_os
-- once inside psql, paste the contents of /schema.sql and press Enter
-- inside psql, run: \q to quit when finished
```

If you prefer a one-liner to execute the file directly:

```powershell
docker exec -i biz-os-db psql -U bizadmin -d ai_business_os -f /schema.sql
```

## Environment

Copy `backend/.env.example` to `backend/.env` and update secrets as needed. Make sure `DB_PASSWORD` matches the `POSTGRES_PASSWORD` used when creating the container (default above: `bizpass123`).

## Run the backend

```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Notes

- The `database/schema.sql` file contains CREATE EXTENSION and DDL for `vendors`, `invoices`, `invoice_items`, and `documents`, plus sample rows to seed the DB.
- The `MISTRAL_API_KEY` environment variable is required for the assistant route to call the Mistral API.
