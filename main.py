import asyncio


from tg_bot import NewsMakeBot
from asyncio import create_task






class BotCore:

    news_bot = NewsMakeBot()



    async def main(self):

        monitoring = create_task(self.news_bot.news_monitoring())
        bot_on = create_task(self.news_bot.bot.polling())
        await asyncio.gather(monitoring, bot_on)


if __name__ == '__main__':
    bc = BotCore()
    asyncio.run(bc.main())
