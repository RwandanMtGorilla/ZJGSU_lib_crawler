from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options
import json
import time
import os
import shutil
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import ipaddress


class Crawler:
    def __init__(self, start_url, max_depth=2):
        self.visited = set()
        self.base_url = start_url
        self.max_depth = max_depth
        self.counter = 0
        self.site_structure = {}
        # 设置无头模式
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.page_load_strategy = 'none'

        self.driver = webdriver.Chrome(options=chrome_options)
        self.site_structure = self.recursive_crawl(start_url)

    def save_structure(self):
        # 创建一个备份
        if os.path.exists('site_structure.json'):
            shutil.copy('site_structure.json', 'site_structure_backup.json')
        with open('site_structure.json', 'w') as f:
            json.dump(self.site_structure, f, indent=4)

    def is_internal_link(self, url):
        netloc = urlparse(url).netloc
        try:
            # 检查是否是IPv4地址
            ipaddress.IPv4Address(netloc)
            return True
        except ipaddress.AddressValueError:
            # 如果不是IPv4地址，检查域名是否包含“zjgsu”
            return "zjgsu" in netloc

    def normalize_url(self, url):
        # 解析URL
        parsed_url = urlparse(url)
        # 对查询参数进行排序
        sorted_query = sorted(parse_qs(parsed_url.query).items())
        # 重新构建URL
        return urlunparse(parsed_url._replace(query=urlencode(sorted_query, True)))

    def recursive_crawl(self, url, depth=1, link_text=None, current_url=None):
        # 确保URL是标准化的
        url = urljoin(current_url or self.base_url, url)
        normalized_url = self.normalize_url(url)
        result = {
            'title': None,
            'url': normalized_url,
            'children': [],
            'link_text': link_text
        }
        if normalized_url in self.visited or depth > self.max_depth:
            return result
        self.visited.add(normalized_url)

        try:
            self.driver.get(url)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            title_tag = soup.find('title')
            result['title'] = title_tag.string if title_tag else None
            print(f"{'-' * depth} {result['title']} ({url})")

            if self.is_internal_link(url):
                for a_tag in soup.find_all('a', href=True):
                    # 使用当前页面的URL作为基础URL解析相对URL
                    next_url = urljoin(url, a_tag['href'])
                    if next_url not in self.visited:
                        child_result = self.recursive_crawl(next_url, depth + 1, a_tag.get_text(strip=True), url)
                        result['children'].append(child_result)

                        self.counter += 1
                        if self.counter % 10 == 0:
                            self.save_structure()

        except Exception as e:
            print(f"Error while crawling {url}: {e}")

        return result

    def close(self):
        self.driver.quit()

# 示例使用
crawler = Crawler("http://www.zjgsu.edu.cn/11/")
crawler.save_structure()  # 爬取完成后再次保存确保数据完整性
crawler.close()
