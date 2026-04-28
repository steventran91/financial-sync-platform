from sqlalchemy import Column, DateTime, String, Integer, Numeric, ForeignKey
from backend.app.db.base import Base


class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    amount = Column(Numeric, nullable=False)
    merchant = Column(String, nullable=False)
    status = Column(String, nullable=False)
    sync_job_id = Column(Integer, ForeignKey("sync_jobs.id"), nullable=False)