from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///events.db')
Session = sessionmaker(bind=engine)

class EventModel(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event_name = Column(String)
    event_type = Column(String)
    location = Column(String)
    address = Column(String)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    description = Column(String)
    enhanced_description = Column(String)
    image_urls = Column(JSON)
    hash_tags = Column(JSON)
    keywords = Column(JSON)
    visit_tip = Column(String)
    target_audience = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    source_url = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

Base.metadata.create_all(engine)