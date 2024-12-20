# backend/services/image_handler.py
import requests
from PIL import Image
from io import BytesIO
import os
from datetime import datetime

class ImageHandler:
    def __init__(self):
        self.cache_dir = 'cache/images'
        os.makedirs(self.cache_dir, exist_ok=True)

    def optimize_image(self, image_url: str, max_width: int = 800) -> str:
        try:
            # 캐시 확인
            cache_path = self._get_cache_path(image_url)
            if os.path.exists(cache_path):
                return cache_path

            # 이미지 다운로드
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            # 리사이징
            if image.width > max_width:
                ratio = max_width / image.width
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height), Image.LANCZOS)

            # 최적화 및 저장
            image.save(cache_path, 'JPEG', quality=85, optimize=True)
            return cache_path

        except Exception as e:
            print(f"Error optimizing image: {str(e)}")
            return None

    def _get_cache_path(self, url: str) -> str:
        # URL을 파일명으로 변환
        filename = f"{hash(url)}.jpg"
        return os.path.join(self.cache_dir, filename)