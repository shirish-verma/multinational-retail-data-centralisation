import time
import urllib.request
from selenium import webdriver

def extract_links(driver: webdriver, animal: str, root: str) -> list:
    URL = root + animal
    driver.get(URL)
    animal_list = driver.find_elements_by_xpath('//figure[@itemprop="image"]')
    links = []
    for item in animal_list:
        links.append(item.find_element_by_xpath('.//a').get_attribute('href'))
    return links

def get_image_source(driver: webdriver, link: str) -> str:
    driver.get(link)
    time.sleep(0.5)
    src = driver.find_element_by_xpath('//img[@class="oCCRx"]').get_attribute('src')
    return src

def download_images(src: str, animal: str, i: int) -> None:
    urllib.request.urlretrieve(src, f"{animal}_{i}.jpg")


animal = 'cat'
root = 'https://unsplash.com/s/photos/'
driver = webdriver.Chrome()
links = extract_links(driver, animal, root)
for i, link in enumerate(links):
    src = get_image_source(driver, link)
    download_images(src, animal, i)