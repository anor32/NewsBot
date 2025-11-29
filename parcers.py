import re

import bs4
import httpx
from bs4 import BeautifulSoup


class NewsParser:
    url = 'https://www.warhammer-community.com/en-gb/'
    def parce(self,number_news=0) -> str:
        source = httpx.get(url=self.url)
        soup = BeautifulSoup(source.text,'lxml')
        news_list = soup.find('ul',class_='row flex flex-wrap gap-y-10 md:gap-y-20 xl:gap-y-30')
        s = news_list.find_all('li',class_='column w-full md:!w-6/12 lg:!w-4/12 xl:!w-3/12')
        news = s[number_news]
        link = news.find('a',class_='btn-cover mb-15 md:mb-20 block link-underline link-underline--light')
        image = news.find('img').get('src')

        bad_url = self.url+ link.get('href')
        good_url = re.sub(r'en-gb//en-gb/', 'en-gb/', bad_url)


        return (good_url, image)

