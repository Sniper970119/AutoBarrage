# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from config import *
import time
import requests
import pickle
import io


def login(url):
    driver.get(url)
    driver.maximize_window()
    print(driver.title)
    time.sleep(1)
    # #js-header > div > div > div.Header-right > div.Header-login-wrap > div > div > div > div > div > a:nth-child(3)
    # #js-header > div > div > div.Header-right > div.Header-login-wrap > div > a:nth-child(2)
    # #js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > div.MuteStatus.is-noLogin > span
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    "#js-header > div > div > div.Header-right > div.Header-login-wrap > div > div > a > span")))
    print('找到登录按钮')
    # 点击登录按钮
    login_button.click()

    # 这个时候我们用二维码登录，设置最多等待3分钟，如果登录那个区域是可见的，就登录成功
    # 检查是否登录成功
    WebDriverWait(driver, 180).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          "#js-header > div > div > div.Header-right > div.Header-login-wrap > div > a > span > div > div")))

    print("登录成功")
    # 保存cookie到cookies.pkl文件
    session = requests.Session()
    # 获取cookie
    cookies = driver.get_cookies()
    # 把cookie写入文件
    if not os.path.exists("cookie"):
        os.mkdir("cookie")
    pickle.dump(cookies, io.open("./cookie/cookies.pkl", "wb"))


def login_with_cookie(url):
    driver.get("https://www.douyu.com")
    # 把cookie文件加载出来
    with io.open("./cookie/cookies.pkl", "rb") as cookiefile:
        cookies = pickle.load(cookiefile)
    for cookie in cookies:
        # print(cookie)
        driver.add_cookie(cookie)
    time.sleep(3)
    driver.get(url)
    # 如果cookie没有登录成功，退出程序
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "#js-header > div > div > div.Header-right > div.Header-login-wrap > div > a > span > div > div")))
    except:
        print("对不起，使用cookie登录失败，请先删除cookies文件再重新登录")
        os._exit(0)
    print("登录成功")
    print(driver.title)


def send_barrage():
    file = io.open("danmu.dm", mode='r', encoding='utf-8')
    while (True):
        print('开始发送弹幕')
        line = file.readline()
        if not line:
            file.seek(0)
            continue
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > textarea"))).send_keys(
            line)

        time.sleep(TIME)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > div"))).click()
        # 清空输入框信息
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > textarea"))).clear()
        print(line)


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "https://www.douyu.com",
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    # 修改chrome配置
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path="./driver/win/chromedriver.exe", chrome_options=options)

    # 隐式等待是全局性的，只要用了driver.findxx没有第一时间找到元素，就会等待5s，当然一般都被用wait覆盖掉了
    driver.implicitly_wait(5)
    # 显示等待是定向性的，最大等待时间10s,每次检测元素有没有生成的时间间隔300ms，过了最大等待时间抛出异常
    wait = WebDriverWait(driver, timeout=10, poll_frequency=300)

    url = 'https://www.douyu.com/' + ROOM_ID

    if os.path.exists("./cookie/cookies.pkl"):
        print("存在Cookies，自动登录")
        login_with_cookie(url)
    else:
        print("不存在cookie，手动登录")
        login(url)
    send_barrage()
