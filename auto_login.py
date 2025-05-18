# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00CA5BB95D31953D2946805105897A2CB4A0254A8E05E9D22882CDCD932862726833FD649A4087C09DC42535F8EE79368CAF7CD7C9C9B0B7BCC2ED3748598072B70F6423A6BACABE366DDF32EA9CED2AB7918EEF91CDDCDDC0A38744E01F789C4D3D230D8403A9C3472A704D050BC5418651E87DAF48E4F9EA2E9C069D52BAF17C0AAECAFC6ADE8A0A7D206FF174B7578BDF0F0E3230C6E45B1E7043D22124500616BFCDB9E1D990F8E6F9875DD037A49F5DA227C1EB048C7DBE89AB9E5417EC5AE9890DDE4ECC0E51E6309693C63477245F56E5AAF5FE4E2CA7807B4E1A4D1DC3C9A53F5ED190079FB5056FC991AB2EFCF8993A604E937859E6D3B1E1312D6E1E007DC4641DA67237213BF5BE865E8F3EC15CE7117494CC3239F2291D35E9E7B4776683637294F0CF9678F6BB5DE9FDDFC7341D13BCB2BAE7E6EB1092E42DCD1E669C2405F213CCD43BC97D0D618A682F9943086FB7ECB1CA878D5CEFD46DCDAE"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
