# backend/services/sitemap_generator.py
from datetime import datetime
import xml.etree.ElementTree as ET

class SitemapGenerator:
    def generate_sitemap(self, events):
        urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        
        # 홈페이지
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = 'https://your-domain.com'
        ET.SubElement(url, 'changefreq').text = 'daily'
        ET.SubElement(url, 'priority').text = '1.0'
        
        # 각 이벤트 페이지
        for event in events:
            url = ET.SubElement(urlset, 'url')
            ET.SubElement(url, 'loc').text = f'https://your-domain.com/event/{event.id}'
            ET.SubElement(url, 'lastmod').text = event.updated_at.strftime('%Y-%m-%d')
            ET.SubElement(url, 'changefreq').text = 'daily'
            ET.SubElement(url, 'priority').text = '0.8'
        
        return ET.tostring(urlset, encoding='unicode', method='xml')