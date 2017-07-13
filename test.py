import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from xvfbwrapper import Xvfb

SEARCH_NAME = "PSY Gangnam"
URL = 'https://www.youtube.com/results?q={}&sp=CAM%253D'.format(SEARCH_NAME)
EXTENSION = "adblockpluschrome-1.13.3.1789.crx"
RESULTS_PAGE_LOCATOR = "results"
AD_LOCATOR = "videoAdUiProgressBar"
VIDEO_NAME_LOCATOR = "eow-title"
NEXT_BUTTON = "//*[@class='ytp-next-button ytp-button']"
FIRST_ELEMENT_OF_RESULTS = "//*[@id='results']/*/*/*/li[2]/div/div/div[2]/h3"

DELAY = 10
VIDEO_TRIES = 11


def setup(with_adblock=False):
    chop = None
    if with_adblock:
        chop = webdriver.ChromeOptions()
        chop.add_extension(EXTENSION)
    driver = webdriver.Chrome(chrome_options=chop)
    driver.maximize_window()
    driver.implicitly_wait(DELAY)
    return driver


def get_text():
    return driver.find_element_by_id(VIDEO_NAME_LOCATOR).text


def find_ad():
    ad = False
    try:
        ad = WebDriverWait(driver, DELAY).until(
            EC.presence_of_element_located((By.CLASS_NAME, AD_LOCATOR)))
        if ad:
            time.sleep(DELAY)
            ad = True
    except:
        pass
    return ad


def check_if_videos_has_ad():
    for i in range(VIDEO_TRIES):
        check = find_ad()
        video_name = "{} has ad: {}".format(get_text(), check)
        driver.save_screenshot("screenshots/{}{}.png".format(video_name[0:15], check))
        if i < VIDEO_TRIES:
            driver.find_element_by_xpath(NEXT_BUTTON).click()
        print(video_name)


def navigate_to_results():
    driver.get(URL)
    WebDriverWait(driver, DELAY).until(
        EC.presence_of_element_located((By.ID, RESULTS_PAGE_LOCATOR))
    )


with Xvfb() as xvfb:
    print('-' * 7 + ' Starting test without adblock ' + '-' * 7 + '\n')
    driver = setup()
    navigate_to_results()
    first_video = driver.find_element_by_xpath(FIRST_ELEMENT_OF_RESULTS)
    first_video.click()
    check_if_videos_has_ad()
    driver.quit()

    print('\n' + '-' * 7 + ' Starting test with adblock ' + '-' * 7 + '\n')
    driver = setup(with_adblock=True)
    navigate_to_results()
    first_video = driver.find_element_by_xpath(FIRST_ELEMENT_OF_RESULTS)
    first_video.click()
    check_if_videos_has_ad()
    driver.quit()
