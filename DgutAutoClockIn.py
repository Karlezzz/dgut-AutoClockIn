# # -*- coding: utf-8 -*-
import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from selenium import webdriver
from selenium.webdriver.common.by import By

result = "还未打卡"
try:

    option = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=option)
    browser.implicitly_wait(10)
    browser.get("https://yqfk-daka.dgut.edu.cn/")
    browser.implicitly_wait(10)
    time.sleep(10)

    browser.find_element(By.ID, "username").send_keys("--此处输入学号--")  # 输入学号
    browser.find_element(By.ID, "password").send_keys("--此处输入密码--\n")  # 输入密码并登录
    time.sleep(10)

    browser.execute_script("document.querySelectorAll('.van-cell__title')[7].click()")  # 点击选择身体状况选项
    time.sleep(1)
    browser.execute_script("document.querySelector('.van-picker__confirm').click()")  # 提交身体状况
    time.sleep(1)

    element_body_temperature = browser.find_element(By.TAG_NAME, 'textarea')
    element_body_temperature.send_keys(Keys.CONTROL, 'a')  # 清空体温
    element_body_temperature.send_keys('36.5')  # 输入体温
    time.sleep(1)

    browser.execute_script("document.querySelectorAll('.van-cell__title')[10].click()")  # 点击选择是否在校
    time.sleep(1)
    browser.execute_script("document.querySelectorAll('.van-picker__confirm')[1].click()")  # 提交在校情况
    time.sleep(1)

    browser.execute_script("document.querySelectorAll('.van-cell__title')[36].click()")  # 选择最后一次核酸日期
    time.sleep(1)
    browser.execute_script("document.querySelectorAll('.van-picker__confirm')[2].click()")  # 提交核酸日期
    time.sleep(1)

    # 提交打卡并且判断打卡结果
    js_code = "let a = document.createElement('p');" \
              "let b = document.createTextNode('已经打过卡了');" \
              "let c = document.createTextNode('打卡成功');" \
              "let d = document.createTextNode('打卡失败');" \
              "let content = document.querySelector('button').querySelector('span').innerHTML;" \
              "if(content === '提交'){document.querySelector('button').click();a.appendChild(c);}" \
              "else if(content === '撤回重填') a.appendChild(b);" \
              "let timer = setInterval(function () {let content1 = document.querySelector('button').querySelector('span').innerHTML;if (content1 === '提交') a.appendChild(d);else if (content1 === '撤回重填') a.appendChild(b);document.body.appendChild(a);clearInterval(timer);}, 20000);"
    browser.execute_script(js_code)
    time.sleep(30)

    print(browser.find_element(By.XPATH, "//p").text)
    if browser.find_element(By.XPATH, "//p").text == "已经打过卡了":
        result = "已经打过卡"
    elif browser.find_element(By.XPATH, "//p").text == "打卡成功已经打过卡了":
        result = "打卡成功"
    else:
        result = '打卡失败'

    time.sleep(3)
    browser.quit()

except:
    result = "打卡失败"

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
EmailDate = str(now)
EmailTile = '我自己' + result
msg = MIMEText(result, 'html', 'utf-8')  # 正文
msg['From'] = formataddr([EmailTile, "--此处输入你的邮箱--"])  # 发信人
msg['Subject'] = EmailDate  # 标题
server = smtplib.SMTP_SSL("smtp.qq.com")
server.login("--此处输入你的邮箱--", "--此处输入你的邮箱密钥--")  # 发件人 密钥
server.sendmail("--此处输入你的邮箱--", "--此处输入你的邮箱--", msg.as_string())
server.quit()
