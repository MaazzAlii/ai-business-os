from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, Numeric, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(Text, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(Text, nullable=False, default="pending")
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
