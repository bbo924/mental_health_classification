from bs4 import BeautifulSoup
# 1. Using selenium
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import re

# browser = webdriver.Chrome(ChromeDriverManager().install())
# browser.get('https://www.dailystrength.org/group/depression')
# browser.implicitly_wait(3)
# time.sleep(3)
# browser.find_element_by_xpath('//*[@id="load-more-discussions"]').click()
# i = 0
# for i in range(2):##这里设置点击5次“加载更多”
#     print(i)
#     browser.find_element_by_xpath('//*[@id="load-more-discussions"]').click()
#     time.sleep(5)###如果网页没有完全加载，会出现点击错误，会点击到某个电影页面，所以加了一个睡眠时间。
#     ##browswe.page_source是点击5次后的源码，用Beautiful Soup解析源码
#     soup = BeautifulSoup(browser.page_source, 'html.parser')

# # //*[@id="main-content"]/section/div[3]/div[1]/div/div[2]/ul/li[1]
# # //*[@id="ds-3816235"]
# for link in soup.find_all('a'):
#     print(link.get('href'))
# # items = soup.find('div', class_=re.compile('list-wp'))
# # for item in items.find_all('a'):
# #     Title = item.find('span', class_='title').text
# #     Rate = item.find('span', class_='rate').text
# #     Link = item.find('span',class_='pic').find('img').get('src')
# #     print(Title,Rate,Link)

import requests
from requests.exceptions import RequestException
import time
import csv
import json

# 2. Parsing url link
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        print("FAILED")

def parse_pages(url_list):
    for url in url_list:
        try:
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                return response.json()
            return None
        except RequestException:
            print("FAILED")

def save(infos):
    # save to csv file
    with open('depression.csv', 'a', newline='',encoding='utf-8') as f:
        fieldnames = ['Title', 'Director', 'Actors', 'Rate', 'Link']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in parse_one_page(d):
            writer.writerow(item)
    pass

def main():
    for i in range(10): ##!!! when to stop
        url = 'https://www.dailystrength.org/group/depression/discussions/ajax?page={}&limit=15'.format(i+1)
        d = get_one_page(url)
        print('Finshed page {}'.format(i+1))
        soup = BeautifulSoup(d['content'], "html.parser")
        tags = soup.find_all(id = re.compile("^ds"))
        url_list = []
        for tag in tags:
            post_url = tag["href"]
            url_list.append("https://www.dailystrength.org" + post_url)

        # get title and text for one group posts 
        infos = parse_pages(url_list)
        # dynamically save one groups info into depression.csv
        save(infos)
            
if __name__=='__main__':
    main()