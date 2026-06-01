-- PostgreSQL schema for AI Business OS (expanded)
-- Ensure UUID generator is available for gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS vendors (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name       VARCHAR(255) NOT NULL,
    email      VARCHAR(255),
    phone      VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invoices (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id      UUID REFERENCES vendors(id),
    invoice_number VARCHAR(100),
    invoice_date   DATE,
    due_date       DATE,
    total_amount   NUMERIC(12,2),
    currency       VARCHAR(10) DEFAULT 'PKR',
    status         VARCHAR(20) DEFAULT 'unpaid'
                   CHECK (status IN ('unpaid','paid','overdue','cancelled')),
    pdf_filename   VARCHAR(255),
    raw_text       TEXT,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invoice_items (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id   UUID REFERENCES invoices(id) ON DELETE CASCADE,
    description  TEXT,
    quantity     NUMERIC(10,2),
    unit_price   NUMERIC(12,2),
    total_price  NUMERIC(12,2),
    category     VARCHAR(50) DEFAULT 'other'
                 CHECK (category IN (
                     'supplies','services','equipment',
                     'shipping','utilities','other'
                 ))
);

CREATE TABLE IF NOT EXISTS documents (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename    VARCHAR(255) NOT NULL,
    doc_type    VARCHAR(50) DEFAULT 'general',
    uploaded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_invoices_status   ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_invoices_due_date ON invoices(due_date);
CREATE INDEX IF NOT EXISTS idx_invoices_vendor   ON invoices(vendor_id);

-- Sample data so the AI assistant has something to answer about
INSERT INTO vendors (id, name, email) VALUES
  ('a1b2c3d4-0000-0000-0000-000000000001','Ali Traders','ali@traders.pk'),
  ('a1b2c3d4-0000-0000-0000-000000000002','Karachi Supplies Co.','info@karsupply.pk'),
  ('a1b2c3d4-0000-0000-0000-000000000003','Lahore Paper Mills','orders@lpm.pk')
ON CONFLICT DO NOTHING;

INSERT INTO invoices
    (vendor_id,invoice_number,invoice_date,due_date,total_amount,status)
VALUES
  ('a1b2c3d4-0000-0000-0000-000000000001','INV-2026-001','2026-05-10','2026-05-25',45000,'unpaid'),
  ('a1b2c3d4-0000-0000-0000-000000000002','INV-2026-002','2026-05-15','2026-05-30',128500,'unpaid'),
  ('a1b2c3d4-0000-0000-0000-000000000001','INV-2026-003','2026-04-20','2026-05-05',22000,'paid'),
  ('a1b2c3d4-0000-0000-0000-000000000003','INV-2026-004','2026-05-01','2026-05-20',67300,'overdue'),
  ('a1b2c3d4-0000-0000-0000-000000000002','INV-2026-005','2026-05-28','2026-06-15',93000,'unpaid')
ON CONFLICT DO NOTHING;

INSERT INTO invoice_items
    (invoice_id,description,quantity,unit_price,total_price,category)
SELECT id,'Leather raw material',100,450,45000,'supplies'
FROM invoices WHERE invoice_number='INV-2026-001';

INSERT INTO invoice_items
    (invoice_id,description,quantity,unit_price,total_price,category)
SELECT id,'Office stationery',50,120,6000,'supplies'
FROM invoices WHERE invoice_number='INV-2026-002';

INSERT INTO invoice_items
    (invoice_id,description,quantity,unit_price,total_price,category)
SELECT id,'Delivery charges',1,2500,2500,'shipping'
FROM invoices WHERE invoice_number='INV-2026-002';
