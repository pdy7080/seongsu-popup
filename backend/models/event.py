from datetime import datetime
from typing import List, Optional

class Event:
    def __init__(self):
        self.id: Optional[int] = None
        self.event_name: str = ""
        self.event_type: str = ""
        self.location: str = ""
        self.address: str = ""
        self.period_start: Optional[datetime] = None
        self.period_end: Optional[datetime] = None
        self.description: str = ""
        self.enhanced_description: str = ""
        self.image_urls: List[str] = []
        self.hash_tags: List[str] = []
        self.keywords: List[str] = []
        self.visit_tip: str = ""
        self.target_audience: str = ""
        self.latitude: Optional[float] = None
        self.longitude: Optional[float] = None
        self.source_url: str = ""
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'event_name': self.event_name,
            'event_type': self.event_type,
            'location': self.location,
            'address': self.address,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'description': self.description,
            'enhanced_description': self.enhanced_description,
            'image_urls': self.image_urls,
            'hash_tags': self.hash_tags,
            'keywords': self.keywords,
            'visit_tip': self.visit_tip,
            'target_audience': self.target_audience,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'source_url': self.source_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }