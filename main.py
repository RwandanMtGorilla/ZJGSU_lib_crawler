import urllib.parse

from Fetchhtml_extract import search_articles,search_articles_n, filter_and_get_final_urls
from DownPDF import download_pdf
import json

query = "土豆"
maxNum = 40

# 使用函数进行搜索，并获取结果
results = search_articles_n(query,maxNum)
print('搜索结果:', results)

search_page_url = f"http://jour.zjgsu.superlib.net"
final_urls = filter_and_get_final_urls(results)
print('最终结果:', final_urls)

for url in final_urls:
    article_url = url
    download_pdf(article_url)
