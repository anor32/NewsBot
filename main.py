import asyncio
from time import sleep
from gemini_api import GeminiNews
from parcers import NewsParser
from tg_bot import NewsMakeBot
from asyncio import create_task

np = NewsParser()

gemini = GeminiNews()


class BotCore:
    interval = 120
    url = ''
    news_bot = NewsMakeBot()

    async def news_monitoring(self):
        while True:
            news_url = np.parce()
            if self.url != news_url:
                self.url = news_url
                await self.prepare_news(news_url)
            await asyncio.sleep(self.interval)

    async def prepare_news(self, url=None):
        if url:
            gemini_prompt = f"""{url} на основе этой ссылки сделай новость для телеграмма добавь хештеги используй 
                   html теги для красивой обработки текста """

            news_text = gemini.make_news_with_gemini(gemini_prompt)
            self.news_bot.send_news(news_text)

    async def main(self):

        monitoring = create_task(self.news_monitoring())
        bot_on = create_task(self.news_bot.bot.polling(none_stop=True))
        await asyncio.gather(monitoring, bot_on)


if __name__ == '__main__':
    bc = BotCore()
    bc.main()
