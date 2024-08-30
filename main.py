#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options
from requests import post
import uuid
from transliterate import translit

urls = ['https://dzen.ru/news',
        'https://dzen.ru/news/rubric/personal_feed',
        'https://dzen.ru/news/rubric/politics',
        'https://dzen.ru/news/rubric/society',
        'https://dzen.ru/news/rubric/business',
        'https://dzen.ru/news/rubric/svo']

chrome_options = Options()
chrome_options.add_argument('--headless=new')
with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options) as driver:
    for url in urls:
        news_list = []

        driver.get(url)
        sleep(3)

        for news in driver.find_elements(By.CLASS_NAME, 'news-site--card-top-avatar__rootElement-1U'):
            elem = BeautifulSoup(news.get_attribute('innerHTML'), 'html.parser')

            news_list.append({'yandex_link': news.get_attribute('href'),
                              'title': elem.find_all('p')[-1].text.replace(u'\xa0', u' '),
                              'link': '',
                              'content': ''})

        for news in driver.find_elements(By.CLASS_NAME, 'news-site--card-news__titleLink-2Q'):
            elem = BeautifulSoup(news.get_attribute('innerHTML'), 'html.parser')

            news_list.append({'yandex_link': news.get_attribute('href'),
                              'title': elem.find('div').text.replace(u'\xa0', u' '),
                              'link': '',
                              'content': ''})

        for news in driver.find_elements(By.CLASS_NAME, 'news-card__link'):
            elem = BeautifulSoup(news.get_attribute('innerHTML'), 'html.parser')

            news_list.append({'yandex_link': news.get_attribute('href'),
                              'title': elem.find_all('span')[1].text.replace(u'\xa0', u' '),
                              'link': '',
                              'content': ''})

    for news in news_list:
        driver.get(news['yandex_link'])
        sleep(3)

        news['link'] = driver.find_element(By.CSS_SELECTOR, '.news-story-head-redesign__title a').get_attribute('href')
        news['content'] = driver.find_element(By.CLASS_NAME, 'news-story-redesign__digest').text.replace('\n', ' ')

        post('http://p729516.ihc.xyz/wordpress/wp-includes/api.php',
             {'post_url': f'{translit(news["title"], "ru", reversed=True).replace(" ", "-")}-{uuid.uuid4()}',
              'post_title': news['title'],
              'post_content': news['content'],
              'news_source': news['yandex_link']})
        print(news)

    sleep(round(3600 / len(urls)))
