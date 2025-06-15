import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import os
from dotenv import load_dotenv

load_dotenv()

# MySQL test database
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "mysql+pymysql://root@localhost:3306/budget_db")
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Drop and recreate all tables for a clean test DB
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Optionally drop tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_database):
    session = TestingSessionLocal()
    yield session
    session.close()

# ... rest of your code remains unchanged ...
