from telebot.async_telebot import  AsyncTeleBot
from telebot import types
import asyncio

from ai_generator import AimlBots
from parcers import NewsParser


class NewsMakeBot:
    user_news = {}
    bot = AsyncTeleBot('7967672239:AAGf5Y7KNol_Ms9lSBP5eq_j25eaIvSaXdw')
    chat_id = '6464072033'
    channel = '@test_channel_bota'
    parser = NewsParser()
    actual_news_url = ''
    ai_bot = AimlBots()

    async def news_monitoring(self):

        while True:
            print('идет мониторинг')
            news_url, image = self.parser.parce()
            if self.actual_news_url != news_url:
                self.actual_news_url = news_url
                await self.prepare_news(news_url,image)
            await asyncio.sleep(self.interval)

    async def prepare_news(self, url=None, image_url = None):
        if url:
            ai_prompt = f"""{url} на основе этой ссылки сделай новость для телеграмма добавь хештеги используй 
                   html теги для парсинга html текста не оставляй ссылку на статью сделай её сам """

            news_text = self.ai_bot.generate_news(prompt=ai_prompt)

            print("Новость подготовлена отправка в бота")
            await self.send_news(news_text,image_url)




    async def send_news(self,news_text,image_url =None):
        btn_approve = types.InlineKeyboardButton(text='Опубликовать', callback_data ="publish")
        btn_cancel = types.InlineKeyboardButton(text='Отмена', callback_data ="сancel")
        markup =types.InlineKeyboardMarkup()
        markup.row(btn_approve,btn_cancel)
        msg =  await self.bot.send_photo(self.chat_id,photo=image_url,caption=news_text,parse_mode='HTML',reply_markup = markup)
        self.user_news[msg.message_id] = news_text




        @self.bot.callback_query_handler(func=lambda call: True)
        async def approve(call):
            message_id = call.message.message_id
            news_text = self.user_news.get(message_id)
            if call.data == 'publish':
                await self.bot.send_message(self.channel, news_text, parse_mode='HTML', )
            elif call.data == 'cancel':
                await self.bot.send_message(self.channel, news_text, parse_mode='HTML', )






