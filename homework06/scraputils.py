import time

import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    news_list: list = []
    tbl_list = parser.table.findAll("table")[1].findAll("tr")
    for i in range(0, len(tbl_list), 3):
        try:
            slov: dict = {}
            slov["title"] = tbl_list[i].findAll("a")[1].string
            slov["author"] = tbl_list[i + 1].find("a").string
            slov["url"] = tbl_list[i].findAll("a")[1].get("href")
            slov["points"] = int(tbl_list[i + 1].findAll("span")[1].string.split()[0])
            slov["comments"] = tbl_list[i + 1].findAll("a")[-1].string.split()[0]
            news_list.append(slov)
        except IndexError:
            continue
    return news_list


def extract_next_page(parser):
    return parser.table.findAll("table")[1].findAll("tr")[-1].contents[2].find("a").get("href")


def get_news(url, n_pages=1):
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        time.sleep(1)
    return news