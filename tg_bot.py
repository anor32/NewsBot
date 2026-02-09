import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio

from ai_generator import AimlBots
from parcers import NewsParser

load_dotenv()
class NewsMakeBot:
    user_news = {}
    chat_id = os.getenv('CHAT_ID')
    bot = AsyncTeleBot(os.getenv('BOT_TOKEN'))
    channel = os.getenv('TG_CHANNEL')
    parser = NewsParser()
    actual_news_url = ''
    ai_bot = AimlBots()

    async def news_monitoring(self, interval=10):
        """проверяет сайт на наличие новых новостей """
        while True:
            print('идет мониторинг новостей')
            news_url, image = self.parser.parce()
            if image == 'Ошибка':
                await  self.bot.send_message(self.chat_id,news_url)
                return news_url , image
            if self.actual_news_url != news_url:
                print('Новая новость подготавливаю к отправке')
                self.actual_news_url = news_url

                await self.prepare_news(news_url, image)
            print('мониторинг закончен')
            await asyncio.sleep(interval)

    async def prepare_news(self, url=None, image_url=None):
        """Подготавливает новость для отправки нейросети """
        if url:
            with open('prompt.txt', 'r', encoding='utf-8') as file:
                ai_prompt = str(file.read()) + str(url)

            news_text = self.ai_bot.generate_news(prompt=ai_prompt)

            print("Новость подготовлена отправка в бота")
            await self.send_news(news_text, image_url)
        else:
            print("Ошибка неправильная ссылка ")

    async def send_news(self, text: str, image_url=None):
        btn_approve = types.InlineKeyboardButton(text='Опубликовать', callback_data="publish")
        btn_regenerate = types.InlineKeyboardButton(text='Перегенерировать', callback_data="regenerate")
        btn_cancel = types.InlineKeyboardButton(text='Удалить', callback_data="cancel")
        markup = types.InlineKeyboardMarkup()
        markup.row(btn_approve, btn_cancel, btn_regenerate)
        try:
            if image_url:
                msg = await self.bot.send_photo(self.chat_id, photo=image_url,
                                                caption=text, parse_mode='HTML',
                                                reply_markup=markup)
            else:
                msg = await self.bot.send_message(self.chat_id, text=text, parse_mode='HTML', reply_markup=markup)

            self.user_news.update({msg.message_id: {'text': text, 'image_url': image_url}})
        except Exception as e:
            error_markup= types.InlineKeyboardMarkup()
            error_markup.row(btn_regenerate,btn_cancel)

            msg = await  self.bot.send_message(self.chat_id,
                                         'Ошибка слишком длинный ответ нейросети или что то другое',
                                         reply_markup=error_markup)
            self.user_news.update({msg.message_id: {'text': text, 'image_url': image_url}})


        @self.bot.callback_query_handler(func=lambda call: True)
        async def action(call):
            message_id = call.message.message_id
            news_text = self.user_news[message_id]['text']
            image_url = self.user_news[message_id]['image_url']
            if call.data == 'publish':
                await self.bot.send_photo(self.channel, photo=image_url, caption=news_text, parse_mode='HTML')

            elif call.data == 'regenerate':
                await self.prepare_news(url=self.actual_news_url, image_url=image_url, )
            elif call.data == 'cancel':
                await self.bot.delete_message(self.chat_id, message_id)
                del self.user_news[message_id]

