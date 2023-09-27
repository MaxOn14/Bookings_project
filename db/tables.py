from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Bookings(Base):
    __tablename__ = 'bookings'
    id: Mapped[int] = mapped_column(primary_key=True)
    booking_date: Mapped[str] = mapped_column(String(256))
    length_of_stay: Mapped[int] = mapped_column(Integer())
    guest_name: Mapped[str] = mapped_column(String(256))
    daily_rate: Mapped[float] = mapped_column(Float())

