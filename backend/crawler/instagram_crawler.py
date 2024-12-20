from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import List
from models.event import Event
from .base_crawler import BaseCrawler  # 이 줄 추가
import time

class InstagramCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.search_tags = ['성수동팝업', '성수팝업', '성수동전시']
        self.driver = None

    def _setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 브라우저 창 숨기기
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def crawl(self) -> List[Event]:
        if not self.driver:
            self._setup_driver()
        
        events = []
        try:
            for tag in self.search_tags:
                url = f"https://www.instagram.com/explore/tags/{tag}/"
                self.driver.get(url)
                time.sleep(3)  # 페이지 로딩 대기

                # 최근 게시물 선택
                posts = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article a"))
                )

                for post in posts[:10]:  # 상위 10개 게시물만 처리
                    try:
                        post.click()
                        time.sleep(2)
                        event = self._parse_post()
                        if event:
                            events.append(event)
                    except Exception as e:
                        print(f"Error processing post: {str(e)}")
                        continue

        finally:
            self.driver.quit()
        
        return events

    def _parse_post(self) -> Event:
        event = Event()
        try:
            # 게시물 텍스트 추출
            text_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div._a9zs"))
            )
            post_text = text_element.text

            # 이벤트 정보 추출
            event.source_url = self.driver.current_url
            event.description = post_text
            
            # 날짜 추출
            event.period_start, event.period_end = extract_date_range(post_text)
            
            # 위치 추출
            event.location = extract_location(post_text)
            
            # 해시태그 추출
            hash_tags = [tag.strip() for tag in post_text.split() if tag.startswith('#')]
            event.hash_tags = hash_tags

            return event if event.location and event.period_start else None

        except Exception as e:
            print(f"Error parsing post: {str(e)}")
            return None