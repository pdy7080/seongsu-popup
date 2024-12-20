from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from .database import Base
from datetime import datetime

class RelatedContent(Base):
    __tablename__ = 'related_contents'

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    sns_posts = Column(JSON)
    blog_posts = Column(JSON)
    news_articles = Column(JSON)
    last_updated = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'event_id': self.event_id,
            'sns_posts': self.sns_posts,
            'blog_posts': self.blog_posts,
            'news_articles': self.news_articles,
            'last_updated': self.last_updated.isoformat()
        }