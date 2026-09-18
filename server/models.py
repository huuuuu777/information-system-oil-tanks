from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Tank(Base):
    __tablename__ = 'tanks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    measurement_date: Mapped[str]
    level_m: Mapped[float]
    fuel_type: Mapped[str] = mapped_column(String(50))
    fuel_volume: Mapped[float]