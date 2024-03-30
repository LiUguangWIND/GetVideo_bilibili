# -*- coding: utf-8 -*-
import time
import requests
import json
import re
import os
from urllib.parse import urlparse
from datetime import datetime

def main():
    # 初始化正则表达式，用于提取视频信息、作者uid和弹幕URL
    regx = r"<script>window.__playinfo__=(.*?)</script>"
    barrage_url_regx = r'value="(https?://[^"]+)"'
    barrage_regx = r'<d p=".*?"(.*?)</d>'
    brief_introduction_regx = r'<input type="text" value="(.*?(\r?\n|.)*?)"'
    regx_1 = r'href="(.*?)/mid(\d+)"'
    base_url_1 = input("输入视频的ID:")
    # 构造请求头中的referer
    referer = f"https://www.bilibili.com/video/{base_url_1}/?"
    current_dateTime = datetime.now()
    print(f"{current_dateTime} 视频防盗链：{referer}")

    # 构造弹幕请求url
    barrage_url_1 = f"https://www.ibilibili.com/video/{base_url_1}/"
    # 定义请求头，用于伪装成浏览器发送请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'Referer': referer
    }
    # 弹幕请求头
    barrage_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'Referer': 'https://api.bilibili.com/'
    }
    # uid请求头
    uid_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.50',
    }

    # 发起请求获取视频页面信息和弹幕信息
    current_dateTime = datetime.now()
    url = f"https://www.bilibili.com/video/{base_url_1}/"
    print(f"{current_dateTime} 视频地址：{url}")
    information = requests.get(url=url, headers=headers)
    if information.status_code == 200:
        # 状态码为200，请求成功
        time.sleep(0)
    else:
        # 状态码不是200，请求未成功
        print(f"请求失败，状态码：{information.status_code}")
        time.sleep(3)
        information = requests.get(url=url, headers=headers)

    html = information.text
    barrage_url_1_response = requests.get(url=barrage_url_1, headers=barrage_headers)
    if barrage_url_1_response.status_code == 200:
        # 状态码为200，请求成功
        time.sleep(0)
    else:
        # 状态码不是200，请求未成功
        print(f"请求失败，状态码：{barrage_url_1_response.status_code}")
        time.sleep(3)
        barrage_url_1_response = requests.get(url=url, headers=headers)

    barrage_url_1_html = barrage_url_1_response.text
    # 提取弹幕URL并请求获取弹幕内容
    barrage_url = re.findall(barrage_url_regx, barrage_url_1_html)[2]
    current_dateTime = datetime.now()
    print(f"{current_dateTime} 弹幕地址:{barrage_url}")
    barrage_url_response = requests.get(url=barrage_url, headers=barrage_headers)
    if barrage_url_response.status_code == 200:
        # 状态码为200，请求成功
        time.sleep(0)
    else:
        # 状态码不是200，请求未成功
        print(f"请求失败，状态码：{barrage_url_response.status_code}")
        time.sleep(3)
        barrage_url_response = requests.get(url=url, headers=headers)

    barrage_url_response.encoding = 'UTF-8'
    barrage_html = barrage_url_response.text

    # 提取图片URL并请求获取图片
    video_face_url = re.findall(barrage_url_regx, barrage_url_1_html)[0]
    current_dateTime = datetime.now()
    print(f"{current_dateTime} 视频封面地址：{video_face_url}")
    video_face_response = requests.get(url=video_face_url, headers=barrage_headers)
    if video_face_response.status_code == 200:
        # 状态码为200，请求成功
        time.sleep(0)
    else:
        # 状态码不是200，请求未成功
        print(f"请求失败，状态码：{video_face_response.status_code}")
        time.sleep(3)
        video_face_response = requests.get(url=url, headers=headers)

    parsed_url_1 = urlparse(video_face_url)
    path_1 = parsed_url_1.path
    # 获取文件名及后缀名
    filename_1, extension_1 = path_1.rsplit('.', 1)
    current_dateTime = datetime.now()
    print(f"{current_dateTime} 视频封面后缀名：{extension_1}")

    # 提取视频信息和弹幕
    video_information = re.findall(regx, html)[0]
    json_video_information = json.loads(video_information)
    barrage_list = re.findall(barrage_regx, barrage_html)
    barrage_content = '\n'.join(barrage_list)

    # 提取音视频资源url和视频标题
    audio_url = json_video_information['data']['dash']['audio'][0]['baseUrl']
    video_url = json_video_information['data']['dash']['video'][0]['baseUrl']
    video_title = re.findall('"title":"(.*?)",', html)[0]
    video_title_cleaned = video_title.strip('"title":').strip('"')
    video_folder_name = video_title_cleaned.replace('"', '').replace('/', '_')  # 替换掉可能导致路径问题的特殊字符

    # 提取作者头像
    video_user_face_url = re.findall(barrage_url_regx, barrage_url_1_html)[1]
    current_dateTime = datetime.now()
    print(f"{current_dateTime} 作者头像地址：{video_user_face_url}")
    video_user_face_response = requests.get(url=video_user_face_url, headers=barrage_headers)
    # 获取文件名及后缀名
    parsed_url_2 = urlparse(video_user_face_url)
    path_2 = parsed_url_2.path
    filename_2, extension_2 = path_2.rsplit('.', 1)
    current_dateTime = datetime.now()
    print(f"{current_dateTime} 作者头像后缀名：{extension_2}")

    # 提取简介
    brief_introduction = re.findall(brief_introduction_regx, barrage_url_1_html)[5]
    current_dateTime = datetime.now()
    brief_introduction = b''.join([item.encode() for item in brief_introduction])
    print(f"{current_dateTime} 已提取简介")

    # 提取uid并请求获取作者信息
    current_dateTime = datetime.now()
    uid_1 = re.findall(regx_1, html)[0]
    UID = uid_1[1]
    print(f"{current_dateTime} 作者uid：{UID}")
    uid_url = f"https://api.bilibili.com/x/web-interface/card?mid={UID}"
    uid_response_1 = requests.get(url=uid_url, headers=uid_headers)
    uid_response = uid_response_1.text
    json_uid_response = json.loads(uid_response)
    name = json_uid_response['data']['card']['name']
    sex = json_uid_response['data']['card']['sex']
    fans = json_uid_response['data']['card']['fans']
    user_informatio = f"用户名：{name}\n性别：{sex}\n粉丝数：{fans}"
    user_informatio = b''.join([item.encode() for item in user_informatio])
    current_dateTime = datetime.now()
    print(f"{current_dateTime} 已成功获取作者信息")

    # 创建目录，如果不存在的话
    directory_path = './' + video_folder_name
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    current_dateTime = datetime.now()
    print(f"{current_dateTime} 视频目录{directory_path}已存在")

    video_result = requests.get(url=video_url, headers=headers).content
    audio_result = requests.get(url=audio_url, headers=headers).content

    # 将音视频资源和弹幕视频封面等内容保存到本地
    current_dateTime_video = datetime.now()
    print(f"{current_dateTime_video} 正在下载视频资源")
    with open(f"{video_title}//" + f"{video_title}(视频资源)" + ".mp4", "wb") as video:
        video.write(video_result)

    current_dateTime_audio = datetime.now()
    print(f"{current_dateTime_audio} 正在下载音频资源")
    with open(f"{video_title}//" + f"{video_title}(音频)" + ".mp3", "wb") as audio:
        audio.write(audio_result)

    current_dateTime_barrage = datetime.now()
    print(f"{current_dateTime_barrage} 正在下载弹幕资源")
    with open(f"{video_title}//{video_title}(弹幕).txt", "wb") as f:
        f.write(barrage_content.encode('utf-8'))

    current_dateTime_video_face = datetime.now()
    print(f"{current_dateTime_video_face} 正在下载视频封面")
    with open(f"{video_title}//" + f"{video_title}(视频封面)" + f".{extension_1}", "wb") as file:
        file.write(video_face_response.content)

    current_dateTime_user_face = datetime.now()
    print(f"{current_dateTime_user_face} 正在下载作者头像")
    with open(f"{video_title}//" + f"{video_title}(作者头像)" + f".{extension_2}", "wb") as file:
        file.write(video_user_face_response.content)

    current_dateTime_brief_introduction = datetime.now()
    print(f"{current_dateTime_brief_introduction} 正在下载视频简介")
    with open(f"{video_title}//" + f"{video_title}(视频简介)" + ".txt", "wb") as f:
        f.write(brief_introduction)

    current_dateTime_uid = datetime.now()
    print(f"{current_dateTime_uid} 正在下载作者信息")
    with open(f"{video_title}//" + f"{video_title}(作者信息)" + ".txt", "wb") as f:
        f.write(user_informatio)

    current_dateTime_finally = datetime.now()
    print(f"\n{current_dateTime_finally} 所有资源已成功下载")

    # 打印下载的资源信息
    print(f"标题：{video_title}")
    print(f"弹幕已保存至：{video_title}（弹幕）.txt")
    print(f"音频链接：{audio_url}")
    print(f"视频链接：{video_url}")

    current_dateTime_finally = datetime.now()
    print(f"\n{current_dateTime_finally} 所有操作已成功完成")

if __name__ == "__main__":
    main()