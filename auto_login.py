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
    browser.add_cookie({"name": "MUSIC_U", "value": "0083D26864FDFDF5042F0A0204503571CCAE969E42790B349543E28D571373AEEC487ADF0D699C271DE32CFA6AD88877C31881D7DA75DEE1A868E1EA975647B2DE4E63137ED43D30CEB3D045942AE4FD0FF6EC626945566593FDC7F0A22B47BAA339A2D30D2C466F6A0155C4F8CB970A4E3E5D3A4CA35351C0F5EC6841CF9BEF70CC7D852B0CA919979F4DBF071DAC73C4391DE2FFB57B1F637B7F1C30C924321885BF4A5210990A22A5BA7F4458C45A2981C1DCCFCD7FE7F9FC5A9C9EDFD61DFEDC1A8DE759F9DCD66C57D47F266C4243B2DB53B3BC422123947A2C0661E2F312846F26320ADEF1FF94C04A223F5C97691EA9E2EE837C8B63BBF5C69A0AF364AC40F6C8D29AD00359575E6D3AEEF2E0E56DF1C39D260D0AC4C697DD21764115FDBB221552A7C5A41BBDAE528447060557233B3D6E91E5B2AF1230EFE908A2B43AB388BBA8D9A980D65D9FDC31D843B7BD7E912B49727021620FBDB44EFC526763"})
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
