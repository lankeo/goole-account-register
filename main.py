import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


def main(user_info):
    options = webdriver.ChromeOptions()
    # 使用headless无界面浏览器模式
    options.add_argument('--headless')  # 增加无界面选项
    options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
    options.add_argument('--incognito')  # 无痕模式
    options.add_argument(
        '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/95.0.4638.54 Safari/537.36"')
    options.add_argument('--lang=en')
    # options.add_argument('--blink-settings=imagesEnabled=false')  # 禁止加载图片

    browser = webdriver.Chrome(chrome_options=options)
    browser.maximize_window()

    main_url = "https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp"
    browser.get(main_url)

    # 填写信息
    browser.find_element(By.ID, "lastName").send_keys(user_info["last_name"])
    browser.find_element(By.ID, "firstName").send_keys(user_info["first_name"])
    browser.find_element(By.ID, "username").send_keys(user_info["username"])
    browser.find_element(By.NAME, "Passwd").send_keys(user_info["password"])
    browser.find_element(By.NAME, "ConfirmPasswd").send_keys(user_info["password"])
    browser.find_element(By.ID, "accountDetailsNext").find_element(By.CSS_SELECTOR, "button").send_keys(Keys.RETURN)
    time.sleep(5)
    browser.save_screenshot("./google1.png")

    # 短信验证
    browser.find_element(By.ID, "phoneNumberId").send_keys(user_info["phone_code"] + " ")
    # browser.find_element(By.ID, "phoneNumberId").clear()
    time.sleep(2)
    browser.find_element(By.ID, "phoneNumberId").send_keys(user_info["phone"])
    browser.find_element(By.CSS_SELECTOR, ".FliLIb.DL0QTb button").send_keys(Keys.RETURN)
    time.sleep(5)

    browser.save_screenshot("./google2.png")
    msg_code = input("请输入6位短信验证码: G-")
    browser.find_element(By.ID, "code").send_keys(msg_code)
    browser.find_element(By.CSS_SELECTOR, ".FliLIb.DL0QTb button").send_keys(Keys.RETURN)
    time.sleep(5)

    browser.save_screenshot("./google3.png")
    # 填写其他信息
    browser.find_element(By.ID, "phoneNumberId").clear()
    browser.find_element(By.NAME, "recoveryEmail").send_keys(user_info["email"])

    month_opt = browser.find_element(By.ID, "month")
    Select(month_opt).select_by_index(-3)  # 10 月
    browser.find_element(By.ID, "day").send_keys("24")
    browser.find_element(By.ID, "year").send_keys("1991")

    gender_opt = browser.find_element(By.ID, "gender")
    Select(gender_opt).select_by_index(3)  # Rather not say
    browser.find_element(By.CSS_SELECTOR, ".FliLIb.DL0QTb button").send_keys(Keys.RETURN)
    time.sleep(5)

    # 保存截图
    browser.save_screenshot("./google4.png")
    browser.find_element(By.CSS_SELECTOR, ".FliLIb.DL0QTb button").send_keys(Keys.RETURN)
    time.sleep(5)

    res = browser.find_element(By.CSS_SELECTOR, ".x7WrMb").text
    if re.search(r"Welcome, ", res):
        print("注册成功:", res)
    browser.save_screenshot("./googlesuccess.png")
    browser.quit()


if __name__ == '__main__':
    user_info = {
        "last_name": "",
        "first_name": "",
        "username": "",
        "password": "",
        "phone_code": "",
        "phone": ""
    }
    main(user_info)
