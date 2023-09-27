import uvicorn
from fastapi import FastAPI

from funcs import import_data
from db.base import engine
from db.tables import Base
from routers.booking_routers import bookings_db, search, stats, analysis

app = FastAPI(title='Bookings Project')

app.include_router(bookings_db)
app.include_router(search)
app.include_router(analysis)
app.include_router(stats)

if __name__ == "__main__":
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    import_data()
    uvicorn.run("main:app", port=8000, reload=True)