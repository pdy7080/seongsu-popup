from flask import Flask, jsonify
from flask_cors import CORS
from flask_compress import Compress
from models.database import Session, EventModel
from models.related_content import RelatedContent
from crawler.instagram_crawler import InstagramCrawler
from crawler.naver_crawler import NaverCrawler
from services.content_collector import ContentCollector
from services.content_enricher import ContentEnricher
from utils.error_handler import handle_errors
from datetime import datetime
import threading
import schedule
import time

app = Flask(__name__)
CORS(app)
Compress(app)

# 서비스 인스턴스 생성
content_collector = ContentCollector()
content_enricher = ContentEnricher()

@app.route('/api/events', methods=['GET'])
@handle_errors
def get_events():
    session = Session()
    try:
        events = session.query(EventModel).order_by(EventModel.created_at.desc()).all()
        return jsonify([event.to_dict() for event in events])
    finally:
        session.close()

@app.route('/api/events/<int:event_id>', methods=['GET'])
@handle_errors
def get_event(event_id):
    session = Session()
    try:
        event = session.query(EventModel).get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404
            
        return jsonify(event.to_dict())
    finally:
        session.close()

@app.route('/api/events/crawl', methods=['POST'])
@handle_errors
def crawl_events():
    instagram_crawler = InstagramCrawler()
    naver_crawler = NaverCrawler()
    
    events = []
    events.extend(instagram_crawler.crawl())
    events.extend(naver_crawler.crawl())
    
    session = Session()
    try:
        for event in events:
            # 컨텐츠 강화
            enriched_data = content_enricher.enrich_event(event.to_dict())
            
            # 위치-시간 기준으로 중복 체크
            existing = session.query(EventModel).filter_by(
                location=event.location,
                period_start=event.period_start,
                period_end=event.period_end
            ).first()
            
            if not existing:
                event_model = EventModel(**enriched_data)
                session.add(event_model)
        
        session.commit()
        return jsonify({"message": "Crawling completed", "event_count": len(events)})
    finally:
        session.close()

@app.route('/api/events/<int:event_id>/related-content', methods=['GET'])
@handle_errors
async def get_related_content(event_id):
    session = Session()
    try:
        # 캐시된 콘텐츠 확인
        cached_content = session.query(RelatedContent).filter_by(event_id=event_id).first()
        
        if cached_content and (datetime.now() - cached_content.last_updated).total_seconds() < 3600:
            return jsonify(cached_content.to_dict())

        event = session.query(EventModel).get(event_id)
        if not event:
            return jsonify({'error': 'Event not found'}), 404

        content = await content_collector.collect_related_content(
            event.event_name, 
            event.location
        )
        
        if cached_content:
            cached_content.update(content)
        else:
            new_content = RelatedContent(event_id=event_id, **content)
            session.add(new_content)
        
        session.commit()
        return jsonify(content)
    finally:
        session.close()

def run_crawler():
    with app.app_context():
        try:
            crawl_events()
        except Exception as e:
            print(f"Scheduled crawling failed: {str(e)}")

def run_scheduler():
    schedule.every(12).hours.do(run_crawler)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # 스케줄러 시작
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    # Flask 앱 실행
    app.run(debug=True)