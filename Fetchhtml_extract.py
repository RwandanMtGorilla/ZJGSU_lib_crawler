from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Redirect import get_final_url_s
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

search_page_url = f"http://jour.zjgsu.superlib.net"

def search_articles(text):
    # 配置ChromeDriver选项
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无界面模式
    options.add_argument('--disable-gpu')

    # 配置ChromeDriver服务
    service = Service('chromedriver.exe')

    # 初始化WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # 构建目标URL
    url = f"http://jour.zjgsu.superlib.net/searchJour?channel=searchJour&sw={text}&said=0&pid=0&uscol=0&sgcount=0&Field=&qihao=&ecode=utf-8&bCon=&allsw=&sectyear=&jourid=&fenlei=&core=&isort=0&searchtype=&view=0&exp=0&expertsw=&Pages=1"

    # 访问目标URL
    driver.get(url)
    time.sleep(2)  # 等待页面加载

    # 获取页面源代码并关闭浏览器
    page_source = driver.page_source
    driver.quit()

    # 使用BeautifulSoup解析页面
    soup = BeautifulSoup(page_source, 'html.parser')
    articles = soup.find_all('div', class_='book1')

    results = []
    for article in articles:
        article_data = {}

        # 提取标题和链接
        title_tag = article.find('a')
        title = title_tag.get_text(strip=True)
        link = title_tag['href']
        article_data['标题'] = title
        article_data['链接'] = link

        # 提取作者和其他信息
        info_tag = article.find('div', class_='fc-green')
        author_info = info_tag.get_text(strip=True)
        article_data['作者等信息'] = author_info

        # 提取关键词
        keywords = info_tag.find_all('br')[-1].next_siblings
        keywords_text = ''.join(kw.get_text(strip=True) for kw in keywords if hasattr(kw, 'get_text'))
        article_data['关键词'] = keywords_text

        # 提取获取途径
        get_tag = article.find('div', class_='get')
        get_ways = [(a.get_text(strip=True), a['href']) for a in get_tag.find_all('a')]
        article_data['获取途径'] = get_ways

        # 提取隐藏的元素
        hidden_inputs = article.find_all('input', type='hidden')
        hidden_data = {inp['name']: inp['value'] for inp in hidden_inputs}
        article_data['隐藏的信息'] = hidden_data


        results.append(article_data)

    return results

def search_articles_n(text, max_articles=100):
    # 配置ChromeDriver选项

    options = webdriver.ChromeOptions()

    options.add_argument('--headless')  # 无界面模式

    options.add_argument('--disable-gpu')
    # 设置用户代理
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"')

    # 配置ChromeDriver服务
    service = Service('chromedriver.exe')

    # 初始化WebDriver
    print("初始化WebDriver...")
    driver = webdriver.Chrome(service=service, options=options)

    results = []
    page = 1
    total_pages = float('inf')

    while len(results) < max_articles and page <= total_pages:
        # 构建目标URL
        url = f"http://jour.zjgsu.superlib.net/searchJour?channel=searchJour&sw={text}&said=0&pid=0&uscol=0&sgcount=0&Field=&qihao=&ecode=utf-8&bCon=&allsw=&sectyear=&jourid=&fenlei=&core=&isort=0&searchtype=&view=0&exp=0&expertsw=&Pages={page}"

        # 访问目标URL
        print(f"访问URL: {url}")
        driver.get(url)

        # # 使用显式等待
        # wait = WebDriverWait(driver, 10)  # 等待最长10秒
        # element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'book1')))  # 等待class为'book1'的元素加载完成
        # print("页面加载完成")

        page_source = driver.page_source
        print("获取页面源代码完成")

        soup = BeautifulSoup(page_source, 'html.parser')
        print("页面解析完成")
        articles = soup.find_all('div', class_='book1')
        print(f"找到{len(articles)}篇文章")
        # 获取总页数信息

        if page == 1:
            search_info = soup.find('div', id='searchinfo')
            if search_info:
                total_pages_text = re.search(r'共\s*<font[^>]*>\s*(\d+)\s*</font>\s*页', str(search_info))
                if total_pages_text:
                    total_pages = int(total_pages_text.group(1))

        for article in articles:
            if len(results) < max_articles:
                article_data = {}

                # 提取标题和链接
                title_tag = article.find('a')
                title = title_tag.get_text(strip=True)
                link = title_tag['href']
                article_data['标题'] = title
                article_data['链接'] = link

                # 提取作者和其他信息
                info_tag = article.find('div', class_='fc-green')
                author_info = info_tag.get_text(strip=True)
                article_data['作者等信息'] = author_info

                # 提取关键词
                keywords = info_tag.find_all('br')[-1].next_siblings
                keywords_text = ''.join(kw.get_text(strip=True) for kw in keywords if hasattr(kw, 'get_text'))
                article_data['关键词'] = keywords_text

                # 提取获取途径
                get_tag = article.find('div', class_='get')
                get_ways = [(a.get_text(strip=True), a['href']) for a in get_tag.find_all('a')]
                article_data['获取途径'] = get_ways

                # 提取隐藏的元素
                hidden_inputs = article.find_all('input', type='hidden')
                hidden_data = {inp['name']: inp['value'] for inp in hidden_inputs}
                article_data['隐藏的信息'] = hidden_data

                print(article_data)
                results.append(article_data)
            else:
                break

        page += 1

    driver.quit()
    return results

def filter_and_get_final_urls(search_results):
    chaoxing_urls = []
    final_urls = []

    # 遍历搜索结果
    for result in search_results:
        # 检查是否存在获取途径
        if '获取途径' in result:
            # 遍历获取途径
            for way, url in result['获取途径']:
                # 检查获取途径是否为“超星期刊”
                if way == '超星期刊':
                    chaoxing_urls.append(url)

    # 打印找到的“超星期刊”URLs
    print('找到的“超星期刊”URLs:', chaoxing_urls)

    # 对每个“超星期刊”URL执行get_final_url函数
    for url in chaoxing_urls:
        final_url = get_final_url_s(search_page_url, url)
        final_urls.append(final_url)

    # 打印最终的URLs
    print('最终的URLs:', final_urls)

    return final_urls

# 使用函数进行搜索，并获取结果
# results = search_articles("大语言模型")
# print('搜索结果:', results)
#
# search_page_url = f"http://jour.zjgsu.superlib.net"
# final_urls = filter_and_get_final_urls(results)
# print('最终结果:', final_urls)