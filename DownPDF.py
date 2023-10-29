import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os
import re
from requests.exceptions import MissingSchema

def sanitize_filename(filename, max_length=255):
    # 去除不合法的文件名字符
    filename = re.sub(r'[\/:*?"<>|\n\t_]', '', filename)
    # 将空格替换为下划线
    filename = filename.replace(' ', '')
    # 确保文件名长度不会过长
    if len(filename) > max_length:
        extension = filename.split('.')[-1]
        filename = filename[:max_length - len(extension) - 1] + '.' + extension
    return filename


def get_unique_filename(download_dir, filename):
    # 如果文件不存在，直接返回原始文件名
    if not os.path.exists(os.path.join(download_dir, filename)):
        return filename

    # 添加计数器直到找到唯一的文件名
    base, extension = os.path.splitext(filename)
    counter = 1
    while True:
        new_filename = f"{base}_{counter}{extension}"
        if not os.path.exists(os.path.join(download_dir, new_filename)):
            return new_filename
        counter += 1

def download_pdf(article_url, download_dir="download",  base_url="https://qikan.chaoxing.com/"):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        # 检查URL是否有效
    parsed_url = urlparse(article_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f"无效的URL: {article_url}")
        return

    # 发送HTTP GET请求到文章页面
    try:
        response = requests.get(article_url)
        response.raise_for_status()
    except (MissingSchema, requests.exceptions.RequestException) as e:
        print(f"请求失败: {e}")
        return
    # 发送HTTP GET请求到文章页面
    try:
        response = requests.get(article_url)
    except MissingSchema as e:
        print(f"请求失败，无效的URL: {article_url}")
        return
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到文章标题
        title_tag = soup.find('h1', {'class': 'F_titel'})
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            title = "无标题"

        name_tag = soup.find('p', {'class': 'F_name'})
        if name_tag:
            name = name_tag.get_text(strip=True)
        else:
            name = "无名称"

        # 找到来源信息
        div = soup.find('div', class_='Fmian1')
        if div and len(div.find_all('tr')) > 1:
            tr = div.find_all('tr')[1]
            if len(tr.find_all('td')) > 1:
                td = tr.find_all('td')[1]
                a_tag = td.find('a', class_='jourName')
                journal_name = a_tag.text if a_tag else "无期刊信息"
                additional_info = a_tag.next_sibling if a_tag else "无额外信息"
            else:
                journal_name = "无期刊信息"
                additional_info = "无额外信息"
        else:
            journal_name = "无期刊信息"
            additional_info = "无额外信息"

        title= f"{title}-{name}-{journal_name}-{additional_info}"
        title = sanitize_filename(title)

        # 查找所有包含PDF下载链接的<a>标签
        pdf_links = soup.find_all('a', {'class': 'pdfdown'})
        for pdf_link in pdf_links:
            if pdf_link and pdf_link.has_attr('href'):
                # 拼接完整的PDF下载链接
                pdf_url = urljoin(base_url, pdf_link['href'])

                # 发送HTTP GET请求下载PDF
                pdf_response = requests.get(pdf_url)
                if pdf_response.status_code == 200:
                    # 保存PDF文件
                    pdf_filename = get_unique_filename(download_dir, f"{title}.pdf")
                    pdf_path = os.path.join(download_dir, pdf_filename)
                    with open(pdf_path, 'wb') as f:
                        f.write(pdf_response.content)
                    print(f'PDF {title} 下载成功，保存为 {pdf_filename}！')

                    # 创建元文件
                    metadata = {
                        "title": title,
                        "url": article_url,
                        "pdf_url": pdf_url
                    }
                    meta_filename = get_unique_filename(download_dir, f"{title}.json")
                    meta_path = os.path.join(download_dir, meta_filename)
                    with open(meta_path, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, ensure_ascii=False, indent=4)
                    print(f'元文件 {title} 创建成功，保存为 {meta_filename}！')

                    return
                else:
                    print('PDF下载失败，状态码：', pdf_response.status_code)
        print('未找到有效的PDF下载链接')
    else:
        print('文章页面请求失败，状态码：', response.status_code)

# 文章页面的URL
#article_url = "https://qikan.chaoxing.com/detail_38502727e7500f265eafdc6896afed6527581131de457bc81921b0a3ea255101fc1cf1fbb4666ae6aa7de95e2e8c66ac08203281be795e16bdb881d033579da1587e7b9a04b44b0b462fa56f650a2bf5"

# 下载PDF
#download_pdf(article_url)
