from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker



DATABASE_URL = 'sqlite:///./tanks.db'

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)

def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()