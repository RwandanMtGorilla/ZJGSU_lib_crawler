import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def get_final_url_s(base_url, relative_path):
    relative_path = relative_path.strip()
    initial_url = "{}{}".format(base_url, relative_path)

    # 设置Selenium WebDriver的路径
    driver_path = "chromedriver.exe"

    # 设置Chrome选项
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无界面模式
    options.add_argument('--disable-gpu')
    # 创建Service对象
    service = Service(executable_path=driver_path)

    # 启动Selenium WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    # 发送HTTP GET请求
    driver.get(initial_url)

    # 等待页面加载（根据你的网络速度和页面大小调整等待时间）
    time.sleep(5)

    # 获取最终重定向后的URL
    final_url = driver.current_url
    print("最终URL:", final_url)

    # 关闭浏览器
    driver.quit()

    return final_url

def get_final_url(base_url, relative_path):
    relative_path = relative_path.strip()
    # 拼接初始URL
    initial_url = "{}{}".format(base_url, relative_path)

    # 发送HTTP GET请求
    response = requests.get(initial_url)

    # 检查响应状态码
    if response.status_code == 200:
        # 获取最终重定向后的URL
        final_url = response.url
        print("最终URL:", final_url)
        return final_url
    else:
        print("请求失败，状态码：", response.status_code)
        return "Error in fetching final url"

    # search_page_url = f"http://jour.zjgsu.superlib.net"
# # 爬取到的地址
# relative_path = """
# /goreadmaglib.jsp?dxid=100419804767&fenlei=&type=14&d=E116AAC1B3F25BCFD5B1AA9B9B2A9746&timestr=1698486011810
# """# 获取最终的URL
#
#
# get_final_url(search_page_url, relative_path)
