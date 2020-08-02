from bs4 import BeautifulSoup
import re
import requests
from requests.exceptions import RequestException
import time
import csv
import json
import datetime
import sys
import time

# Method 1: Parsing url link (dailyStrength.org)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
def get_one_page(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response
        return None
    except RequestException:
        print("FAILED")

def parse_pages(url_list, condition):
    infos = []
    for url in url_list:
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")
        # date of post
        date = soup.find("time").get_text()
        date_sep = date.split("/")
        post_date = datetime.datetime(int(date_sep[2]), int(date_sep[0]), int(date_sep[1]))
        # make sure correct post date range
        if post_date > datetime.datetime(2017, 12, 31) and post_date < datetime.datetime(2020, 8, 1):
        # if True:
            # find post title and content
            title = soup.find(id="discussion_title").get_text()
            post_contents = soup.find("div", {"class": "posts__content"}).find_all("p")
            post_content = '\n'.join(pc.get_text() for pc in post_contents)
            infos.append([title,post_content,condition])
    return infos

def save(infos):
    # save to csv file
    with open('mental_health.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(infos)

def main():
    condition_list = ['depression','bipolar-disorder','self-injury','eating-disorders','loneliness','multiple-personalities',
                      'adhd-add','personality-disorders','schizophrenia','anger-management','family-friends-of-bipolar',
                      'stress-management','shyness','seasonal-affective-disorder','seasonal-affective-disorder',
                      'post-partum-depression','kleptomania','stuttering','pyromania']
    # condition_list = ['adhd-add','personality-disorders','schizophrenia','anger-management','family-friends-of-bipolar',
    #                   'stress-management','shyness','seasonal-affective-disorder','seasonal-affective-disorder',
    #                   'post-partum-depression','kleptomania','stuttering','pyromania']
    with open('mental_health.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([["Title", "Content", "Mental Condition"]])
    for condition in condition_list:
        for i in range(101): ##!!! when to stop
            # start_time = time.time()
            url = 'https://www.dailystrength.org/group/{}/discussions/ajax?page={}&limit=15'.format(condition, i+1)
            page = get_one_page(url)
            page = page.json()
            # print('Finshed page {}'.format(i+1))
            soup = BeautifulSoup(page['content'], "html.parser")
            tags = soup.find_all(id = re.compile("^ds"))
            url_list = []
            for tag in tags:
                post_url = tag["href"]
                url_list.append("https://www.dailystrength.org" + post_url)

            # get title and text for one group posts 
            infos = parse_pages(url_list,condition)
            # print("--- %s seconds ---" % (time.time() - start_time))
            if len(infos) == 0:
                break
            # dynamically save one groups info into depression.csv
            save(infos)
            
if __name__=='__main__':
    main()


# 2. Using selenium
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import time

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