import json

def get_superstar_url(article_data):
    for article in article_data:
        title = article.get('title', '未知标题')
        get_ways = article.get('get_ways', [])

        for source, url in get_ways:
            print('标题:', title)
            print('超星期刊URL:', url)
            break

# 假设这是你从上一个函数得到的JSON数据
json_data = """
[
    {
        "title": "论语言测试文本的真善美统一",
        "link": "/views/specific/2929/JourDetail.jsp?dxNumber=100272235720&d=E89A3ACD7DA91D683FF54169001E4A49&s=%E6%B5%8B%E8%AF%95%E6%96%87%E6%9C%AC&ecode=utf-8",
        "author_info": "作者：周 胜  付继华刊名：英语教师出版日期：2019期号：第16期ISSN：1009-8852作者单位：佛山科学技术学院关键词：文本；语言测试；真；善；美",
        "keywords": "",
        "get_ways": [
            [
                "超星期刊",
                "/goreadmaglib.jsp?dxid=100272235720&fenlei=&type=14&d=60D2D6D455B9867480F27C5C0649F6F9×tr=1698481650008"
            ],
            [
                "万方(包库)",
                "/goreadmaglib.jsp?dxid=100272235720&aid=550&type=3&d=B55F105D37E6C59FB781FCE65928895F×tr=1698481650003"
            ],
            [
                "维普(包库)",
                "/goreadmaglib.jsp?dxid=100272235720&aid=550&type=4&d=7352289EF7396AEBDF1F710FB53713B5×tr=1698481650003"
            ],
            [
                "CNKI(包库)",
                "/goreadmaglib.jsp?dxid=100272235720&aid=550&type=24&d=062ABD91DF4BCAD7A91560155686B742×tr=1698481650003"
            ],
            [
                "CNKI(镜像)",
                "/goreadmaglibjx.jsp?dxid=100272235720&aid=550&type=24&isjx=true&d=062ABD91DF4BCAD7A91560155686B742×tr=1698481650003"
            ],
            [
                "邮箱接收全文",
                "javaScript:subtoRefer('100272235720','72A069C68FAEE98A648C951BE12BB7AB','1','1698481650008')"
            ]
        ],
        "hidden_data": {
            "f[0].dxid": "100272235720",
            "f[0].title": "论语言<font color=Red>测试文本</font>的真善美统一",
            "f[0].url": "http://jour.zjgsu.superlib.net/views/specific/2929/JourDetail.jsp?dxNumber=100272235720&d=E89A3ACD7DA91D683FF54169001E4A49&s=%E6%B5%8B%E8%AF%95%E6%96%87%E6%9C%AC&ecode=utf-8",
            "f[0].memo": " <b>作者：</b>周 胜  付继华  <b>刊名：</b>英语教师   <b>出版日期：</b>2019   <b>期号：</b>第16期  <b>sIssn：</b>1009-8852  <br><b>关键词：</b><font color=Red>文本</font>；语言<font color=Red>测试</font>；真；善；美<br>"
        }
    },
    {
        "title": "测试文章2",
        "get_ways": [
            ["维普(包库)", "/path/to/article3"],
            ["CNKI(包库)", "/path/to/article4"],
            ["超星期刊", "/path/to/article5"]
        ]
    }
]
"""

# 解析JSON数据
article_data = json.loads(json_data)

# 提取超星期刊的URL
get_superstar_url(article_data)
