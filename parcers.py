import re
from logging import exception

import bs4
import httpx
from bs4 import BeautifulSoup
from bs4.element import AttributeValueList
from requests import ReadTimeout


class NewsParser:
    url = 'https://www.warhammer-community.com/en-gb/'
    def parce(self,number_news=0) -> tuple[str, str] | tuple[str, str ]:
        try:
            source = httpx.get(url=self.url)
        except httpx.ReadTimeout:
            return ("Превышено время ожидания",'Ошибка')
        except Exception  as e:
            print(type(e))
            print('ошибка подключения к сайту')
            return ("Неизвестная ошибка", 'Ошибка')

        soup = BeautifulSoup(source.text,'lxml')
        news_list = soup.find('ul',class_='row flex flex-wrap gap-y-10 md:gap-y-20 xl:gap-y-30')
        s = news_list.find_all('li',class_='column w-full md:!w-6/12 lg:!w-4/12 xl:!w-3/12')
        news = s[number_news]
        link = news.find('a',class_='btn-cover mb-15 md:mb-20 block link-underline link-underline--light')
        image = news.find('img').get('src')

        bad_url = self.url+ link.get('href')
        good_url = re.sub(r'en-gb//en-gb/', 'en-gb/', bad_url)


        return (good_url, image)

