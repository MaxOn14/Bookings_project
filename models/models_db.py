from pydantic import BaseModel, Field


class BookingIn(BaseModel):
    booking_date: str = Field(min_length=10)
    length_of_stay: int = Field(ge=0)
    guest_name: str = Field(min_length=2)
    daily_rate: float = Field(ge=0)

    class Config:
        json_schema = {
            "example": {
                "booking_date": "2015-April-14",
                "length_of_stay": 12,
                "guest_name": "John Green",
                "daily_rate": 20
            }
        }


class BookingOutORM(BookingIn):
    id: int

