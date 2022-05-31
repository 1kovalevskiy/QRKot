from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime

from app.core.db import Base


class CharityProject(Base):
    name = Column(String(100), unique=True)
    description = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now())
    close_date = Column(DateTime)
