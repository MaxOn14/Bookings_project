from typing import Type, List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.base import get_session
from db.tables import Bookings


class BookingCRUD():

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all(self, limit: int, offset: int) -> List[Type[Bookings]]:
        return self.session.query(Bookings).limit(limit).offset(offset).all()

    def create_new(self, dct: dict) -> Bookings:
        try:
            entity = Bookings(**dct)
            self.session.add(entity)
            self.session.commit()
            return entity
        except HTTPException:
            raise HTTPException(status_code=404, detail='Impossible to create')

    def delete(self, booking_id: int) -> Type[Bookings]:
        data = self.session.query(Bookings).filter(Bookings.id == booking_id).first()
        if data is not None:
            self.session.delete(data)
            self.session.commit()
            return data
        else:
            HTTPException(status_code=404, detail="Not found")

    def get_one(self, booking_id: int) -> Type[Bookings]:
        data = self.session.query(Bookings).filter(Bookings.id == booking_id).first()
        if data is not None:
            return data
        else:
            raise HTTPException(status_code=404, detail='Booking not found')

    def search(self, booking_date: str,
               length_of_stay: int,
               guest_name: str,
               daily_rate: float) -> List[Type[Bookings]]:
        if booking_date is not None:
            data = self.session.query(Bookings).filter(Bookings.booking_date == booking_date).all()
        elif length_of_stay is not None:
            data = self.session.query(Bookings).filter(Bookings.length_of_stay == length_of_stay).all()
        elif guest_name is not None:
            data = self.session.query(Bookings).filter(Bookings.guest_name == guest_name).all()
        elif daily_rate is not None:
            data = self.session.query(Bookings).filter(Bookings.daily_rate == daily_rate).all()
        if data is not None:
            return data
        else:
            raise HTTPException(status_code=404, detail="Not Found")
