from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine('sqlite:///hotel.db', echo=True)

SessionLocal = sessionmaker(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError:
        session.rollback()
    finally:
        session.close()
        engine.dispose()
