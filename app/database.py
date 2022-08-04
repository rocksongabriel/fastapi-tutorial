from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = \
        "postgresql://darkbotbbl:testpass1234@localhost/myFastAPIDatabase"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


# Dependency to get session connection to the database
def get_db():
    """Yield database session connection."""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
