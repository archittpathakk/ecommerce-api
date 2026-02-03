import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.models import Base  # uses models/__init__.py

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def create_test_database():
    Base.metadata.create_all(bind=engine)


def drop_test_database():
    Base.metadata.drop_all(bind=engine)
