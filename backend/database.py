from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import os

db_dir = "data/db"
if not os.path.exists(db_dir):
    os.makedirs(db_dir)


# Database setup
DATABASE_URL = f"sqlite:///{db_dir}chats.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Database model


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    history = Column(Text, default="[]")  # JSON-encoded chat history
    knowledge_base_ref_pdf = Column(String, nullable=True)  # PDF reference
    knowledge_base_ref_url = Column(
        String, nullable=True)  # File reference or URL


# Create tables if they don't exist
Base.metadata.create_all(bind=engine)
