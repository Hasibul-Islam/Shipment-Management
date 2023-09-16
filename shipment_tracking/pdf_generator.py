from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from PIL import Image
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
def pdf_convertor(chrome_path, url, element_id, file_name ):
    # print(url)
    chrome_driver_path = chrome_path
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1280x800')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument('--lang=en-GB')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument('--log-level=3')

    # chrome_options.add_argument("--incognito")
    ua = UserAgent()
    userAgent = ua.random
    chrome_options.add_argument(f'user-agent={userAgent}')

    chrome_options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})


    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    driver.set_page_load_timeout(3000)
    
    path = os.getcwd()+'\scrape.png'
    print(path)
    # print("from pdf gen: ", url)
    driver.get(url)
    # print('yeah')

    
    el = driver.find_element(By.ID, element_id)
    el.screenshot(path)

    driver.quit()
    
    image_1 = Image.open(path)
    im_1 = image_1.convert('RGB')
    im_1.save(r"{}".format(file_name))