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

    mobileEmulation = {'deviceName': 'Galaxy S5'} #定义移动设备

    option = webdriver.EdgeOptions()
    option.add_experimental_option('mobileEmulation',mobileEmulation) #浏览器模拟移动设备
    browser = webdriver.Edge(options=option)
    browser.implicitly_wait(10)
    browser.get("https://yqfk-daka.dgut.edu.cn/")
    browser.implicitly_wait(10)
    time.sleep(10)

    browser.find_element(By.ID, "username").send_keys("***")  # 输入学号
    browser.find_element(By.ID, "password").send_keys("***\n")  # 输入密码并登录
    time.sleep(10)

    browser.refresh()  # 刷新页面获取ip
    time.sleep(5)

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
    time.sleep(2)

    browser.execute_script("document.querySelectorAll('.van-field__label')[2].click()") #点击校内具体住址
    time.sleep(1)
    browser.execute_script("document.querySelectorAll('.van-cascader__option')[0].click()") #选择学生公寓
    time.sleep(1)
    browser.execute_script("document.querySelectorAll('.van-cascader__option')[6].click()")  # 选择莞华
    time.sleep(1)

    browser.execute_script("document.querySelectorAll('.van-field__label')[13].click()")  # 选择最后一次核酸日期
    time.sleep(5)
    # 7天一周期，七天内都选周期第一天,月份和年份都为最新时间
    # 选择日期
    js_date = """
    let nowDate = new Date().getDate()
    const dateList = [1, 8, 15, 22, 29]
    let selDate = null
    if (nowDate % 7 != 0) selDate = dateList[parseInt(nowDate / 7)]
    else selDate = dateList[parseInt(nowDate / 7 - 1)]
    document.querySelectorAll('.van-picker-column')[4].querySelectorAll('.van-picker-column__item')[selDate - 1].click()
    """
    browser.execute_script(js_date)
    time.sleep(5)
    browser.execute_script("document.querySelectorAll('.van-picker__confirm')[2].click()")  # 提交核酸日期
    time.sleep(1)

    # 提交打卡并且判断打卡结果
    js_confirm = """
    let title1 = document.querySelector('.van-grid-item__icon-wrapper').querySelector('div').innerText
        let button = document.querySelectorAll('button')[1]
        let a = document.createElement('p');
        let b = document.createTextNode('已经打卡');
        let c = document.createTextNode('打卡成功');
        let d = document.createTextNode('打卡异常');
        if(title1.indexOf('未打卡')!=-1||title1.indexOf('撤回今天的打卡')!=-1){
            button.click()
            a.appendChild(c)
        }
        setTimeout(()=>{
            let title2 = document.querySelector('.van-grid-item__icon-wrapper').querySelector('div').innerText
            if(title2.indexOf('未打卡')!=-1||title2.indexOf('撤回今天的打卡')!=-1){
                button.click()
                a.appendChild(d)
            }else if(title2.indexOf('已打卡成功')!=-1){
                a.appendChild(b)
            }
            document.body.appendChild(a)
        },15000)
        """
    
    browser.execute_script(js_confirm)
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
