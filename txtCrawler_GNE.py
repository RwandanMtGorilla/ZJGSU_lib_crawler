import os
import re
import requests
from gne import GeneralNewsExtractor
from readability import Document
import json
import os
from bs4 import BeautifulSoup

# 确保output文件夹存在
if not os.path.exists('output_gne_txt'):
    os.makedirs('output_gne_txt')

# 读取Markdown文件
with open('input.md', 'r', encoding='utf-8') as f:
    content = f.readlines()

# 定义正则表达式来匹配URL
url_pattern = re.compile(r'https?://\S+')

print("开始处理链接...")

# 循环遍历所有的行
for line in content:
    # 查找URL
    url_match = url_pattern.search(line)
    if url_match:
        url = url_match.group()

        # 提取标题和备注
        title = line.split(url)[0].strip('[]* \n')
        remark = line.split(url)[1].strip('[]* \n')

        print(f"找到链接：标题={title}, URL={url}, 备注={remark}")

        # 如果标题和URL存在，获取页面内容
        if title and url:
            try:
                # 发送HTTP请求
                print(f"正在请求：{url}")
                response = requests.get(url)
                response.raise_for_status()

                html = response.content.decode('utf-8')
                extractor = GeneralNewsExtractor()
                result = extractor.extract(html, noise_node_list=['//div[@class="comment-list"]'])

                # 使用readability提取主要内容
                doc = Document(response.content)
                summary = doc.summary()

                soup = BeautifulSoup(summary, 'html.parser')
                # 提取文本内容
                text = soup.get_text(separator='\n', strip=True)

                # 在result字典中添加URL
                result['url'] = url
                result['content_r'] = text

                # 创建文件名，替换文件名中不合法的字符
                safe_title = re.sub(r'[\\/:"*?<>|]+', "", title)
                safe_remark = re.sub(r'[\\/:"*?<>|]+', "", remark) if remark else ""
                filename = f"{safe_title}.json" if not safe_remark else f"{safe_title}_{safe_remark}.json"
                filepath = os.path.join('output_gne_txt', filename)

                # 保存提取的主要内容到文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(result, ensure_ascii=False, indent=4))

                print(f"已保存：{filepath}")
            except requests.RequestException as e:
                print(f"请求失败：{url}，错误：{e}")
        else:
            print("标题或URL缺失，跳过")
    else:
        print("当前行不包含URL，跳过")

print("任务完成")
