import asyncio
from tg_bot import NewsMakeBot
from asyncio import create_task




class BotCore:
    news_bot = NewsMakeBot()
    async def main(self):
        """Запускает функции мониторинга и бота"""
        monitoring = create_task(self.news_bot.news_monitoring(interval=120*60))
        bot_on = create_task(self.news_bot.bot.polling())
        await asyncio.gather(monitoring, bot_on)


if __name__ == '__main__':
    bc = BotCore()
    asyncio.run(bc.main())
