#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
该程序用于在B站（bilbili）上进行搜索，并列出搜索结果的标题和链接。
用户输入搜索关键词，程序将返回包含视频标题和对应视频链接的结果列表。
"""
import requests
import re

def main():
    # 定义正则表达式，用于匹配页面中的标题和链接
    title_regx = r'<h3\b[^>]*>(.*?)</h3>'
    link_regx = r'(?<=href=")[^"]*'

    # 设置分隔符为换行符
    separator = '\n'

    # 搜索的基 URL
    base_url = "https://search.bilibili.com/video?keyword="

    # 获取用户输入的搜索内容
    user_input = input("输入搜索内容：")
    input_text = user_input.replace(' ', '+')  # 将空格替换为加号，以适应URL编码

    # 构造完整的搜索URL
    url = base_url + input_text

    # 设置请求头，伪装为Chrome浏览器访问
    headers = {
        'Referer': 'https://search.bilibili.com/all?',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }

    # 发送GET请求，并获取响应内容
    url_response = requests.get(url=url, headers=headers)
    url_date = url_response.text

    # 使用正则表达式提取标题和链接
    title_list = re.findall(title_regx, url_date)
    link_list = re.findall(link_regx, url_date)

    # 将链接列表转换为字符串，再按换行符分割，以去除重复链接
    link_result = separator.join(link_list)
    links_text = link_result
    all_links = links_text.split('\n')

    # 筛选出有效的视频链接，并去重
    video_link = [link for link in all_links if '//www.bilibili.com/video/' in link]
    video_links_unique = list(dict.fromkeys(video_link))

    # 初始化一个空列表，用于保存格式化后的结果
    formatted_results = []

    # 遍历标题和链接列表，生成格式化结果，并保存到formatted_results中
    for i, (title, link) in enumerate(zip(title_list, video_links_unique)):
        formatted_result = f"结果{i + 1}: {title} {link}"
        formatted_results.append(formatted_result)

    # 将格式化后的结果连接起来，每个结果之间用换行符分隔
    output_text = separator.join(formatted_results)
    # 输出搜索结果
    print(output_text)
    return output_text

if __name__ == "__main__":
    main()