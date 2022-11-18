from sqlalchemy import BigInteger, Column, String, Integer

from bot.db.base import Base

class HistoryEntry(Base):
    __tablename__ = "history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, nullable=False, unique=False, primary_key=True)
    translate_from = Column(String, nullable=False)
    translate_to = Column(String, nullable=False)