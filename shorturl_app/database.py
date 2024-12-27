import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


os.makedirs("./data", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/url.db"

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    with engine.connect() as connection:
        print("Database connection successful")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

except Exception as exception:
    print(f"Error creating database: {exception}")
    raise
