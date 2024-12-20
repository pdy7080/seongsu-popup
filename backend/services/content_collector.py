import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List
import os

class ContentCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.naver_client_id = os.getenv('NAVER_CLIENT_ID')
        self.naver_client_secret = os.getenv('NAVER_CLIENT_SECRET')

    async def collect_related_content(self, event_name: str, location: str) -> Dict:
        """이벤트 관련 콘텐츠 수집"""
        search_query = f"{location} {event_name}"
        
        results = {
            'sns_posts': await self._get_instagram_posts(search_query),
            'blog_posts': await self._get_blog_posts(search_query),
            'news_articles': await self._get_news_articles(search_query)
        }
        
        return results

    async def _get_instagram_posts(self, query: str) -> List[Dict]:
        """Instagram 해시태그 검색 결과"""
        # Instagram Graph API 또는 웹 크롤링으로 구현
        try:
            # 실제 구현시 Instagram API 사용
            return [
                {
                    'id': 'post1',
                    'url': 'https://instagram.com/p/...',
                    'thumbnail': 'image_url',
                    'caption': '게시물 내용...',
                    'likes': 100,
                    'comments': 10
                }
            ]
        except Exception as e:
            print(f"Instagram error: {str(e)}")
            return []

    async def _get_blog_posts(self, query: str) -> List[Dict]:
        """네이버 블로그 검색 결과"""
        try:
            url = "https://openapi.naver.com/v1/search/blog"
            headers = {
                "X-Naver-Client-Id": self.naver_client_id,
                "X-Naver-Client-Secret": self.naver_client_secret
            }
            params = {
                "query": query,
                "display": 5,
                "sort": "date"
            }
            
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            return [
                {
                    'title': item['title'].replace('<b>', '').replace('</b>', ''),
                    'url': item['link'],
                    'description': item['description'],
                    'date': item['postdate']
                }
                for item in data.get('items', [])
            ]
        except Exception as e:
            print(f"Blog search error: {str(e)}")
            return []

    async def _get_news_articles(self, query: str) -> List[Dict]:
        """네이버 뉴스 검색 결과"""
        try:
            url = "https://openapi.naver.com/v1/search/news"
            headers = {
                "X-Naver-Client-Id": self.naver_client_id,
                "X-Naver-Client-Secret": self.naver_client_secret
            }
            params = {
                "query": query,
                "display": 3,
                "sort": "date"
            }
            
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            return [
                {
                    'title': item['title'].replace('<b>', '').replace('</b>', ''),
                    'url': item['link'],
                    'description': item['description'],
                    'date': item['pubDate']
                }
                for item in data.get('items', [])
            ]
        except Exception as e:
            print(f"News search error: {str(e)}")
            return []