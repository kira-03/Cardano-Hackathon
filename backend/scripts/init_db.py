"""
Database initialization script
"""
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings

Base = declarative_base()

class Analysis(Base):
    """Store analysis results"""
    __tablename__ = 'analyses'
    
    id = Column(String, primary_key=True)
    policy_id = Column(String, nullable=False, index=True)
    token_name = Column(String)
    token_symbol = Column(String)
    readiness_score = Column(Float)
    grade = Column(String)
    result_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class MasumiLog(Base):
    """Store Masumi logging records"""
    __tablename__ = 'masumi_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    analysis_id = Column(String, index=True)
    agent_did = Column(String)
    decision_type = Column(String)
    decision_hash = Column(String, unique=True)
    transaction_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Initialize database"""
    print(f"Initializing database at: {settings.database_url}")
    
    engine = create_engine(settings.database_url)
    
    # Create tables
    Base.metadata.create_all(engine)
    
    print("Database initialized successfully!")
    print(f"Tables created: {', '.join(Base.metadata.tables.keys())}")

if __name__ == "__main__":
    init_db()
