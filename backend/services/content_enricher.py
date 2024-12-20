import os
from anthropic import Anthropic
from typing import Dict, Optional
import json

class ContentEnricher:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    def enrich_event(self, event_data: Dict) -> Dict:
        try:
            # 한국어로 더 자연스러운 프롬프트 작성
            prompt = f"""
            다음 성수동 팝업스토어 정보를 매력적인 방문 정보로 발전시켜주세요:

            장소: {event_data.get('location', '성수동')}
            기간: {event_data.get('period_start')} ~ {event_data.get('period_end')}
            기본 설명: {event_data.get('description', '')}

            JSON 형식으로 다음 정보를 제공해주세요:
            1. event_type: 이벤트 유형 (체험형/전시형/할인형/신제품)
            2. enhanced_description: 방문 가치와 특별한 점을 강조한 매력적인 설명 (2-3문장)
            3. hash_tags: 트렌디한 해시태그 5개 (예: #성수동카페 형식)
            4. keywords: 핵심 키워드 3개
            5. visit_tip: 방문 팁 1개
            6. target_audience: 추천 대상
            """

            response = self.anthropic.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                system="You are a Korean pop-up store marketing specialist. Please respond in Korean with JSON format.",
                messages=[{"role": "user", "content": prompt}]
            )

            # JSON 응답 파싱
            enriched_content = json.loads(response.content)
            event_data.update(enriched_content)
            
            return event_data
            
        except Exception as e:
            print(f"Error enriching content: {str(e)}")
            return event_data