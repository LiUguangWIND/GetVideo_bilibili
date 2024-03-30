import os
import time
import video_search
import bilibili_downloader
import logging
import logging.handlers
from PIL import ImageGrab
import pyautogui


# 定义存放错误截图的文件夹路径
screenshot_dir = "error_screenshots"

# 确保文件夹存在，如果不存在则创建
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

def take_screenshot(filename):
    """
    截取当前屏幕并保存为图片
    :param filename: 图片保存路径及名称
    """
    screen = pyautogui.screenshot()
    # 将截图保存到错误截图文件夹内
    full_path = os.path.join(screenshot_dir, filename)
    screen.save(full_path)


def main():
    """
    主函数，执行视频搜索和B站视频下载操作。
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # 设置日志文件handler
    file_handler = logging.handlers.RotatingFileHandler(filename='run.log', maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('程序启动...')

    try:
        # 执行视频搜索主函数
        video_search.main()
        logger.info('搜索完成...')
    except Exception as e:
        # 在发生异常时，截取屏幕并保存
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        screenshot_filename = f'screenshot_{timestamp}.png'
        take_screenshot(screenshot_filename)
        logger.error(f'视频搜索过程中出现异常，已保存截图至 {os.path.join(screenshot_dir, screenshot_filename)}：{e}')

    try:
        # 执行B站下载器主函数
        bilibili_downloader.main()
        logger.info('下载完成...')
    except Exception as e:
        # 在发生异常时，截取屏幕并保存
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        screenshot_filename = f'screenshot_{timestamp}.png'
        take_screenshot(screenshot_filename)
        logger.error(f'B站视频下载过程中出现异常，已保存截图至 {os.path.join(screenshot_dir, screenshot_filename)}：{e}')


# 检查脚本是否直接运行，如果是则执行主函数
if __name__ == "__main__":
    main()
