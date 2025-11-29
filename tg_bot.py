from telebot.async_telebot import AsyncTeleBot
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

    async def news_monitoring(self, interval=10):

        while True:
            print('идет мониторинг новостей')
            news_url, image = self.parser.parce()
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

    async def send_news(self, text, image_url=None):
        btn_approve = types.InlineKeyboardButton(text='Опубликовать', callback_data="publish")
        btn_regenerate = types.InlineKeyboardButton(text='Перегенерировать', callback_data="regenerate")
        btn_cancel = types.InlineKeyboardButton(text='Удалить', callback_data="cancel")
        markup = types.InlineKeyboardMarkup()
        markup.row(btn_approve, btn_cancel, btn_regenerate)
        try:
            if image_url:
                msg = await self.bot.send_photo(self.chat_id, photo=image_url, caption=text, parse_mode='HTML',
                                                reply_markup=markup)

            else:
                msg = await self.bot.send_message(self.chat_id, text=text, parse_mode='HTML', reply_markup=markup)

            self.user_news.update({msg.message_id: {'text': text, 'image_url': image_url}})
        except Exception as e:
            await  self.bot.send_message(self.chat_id, 'Ошибка слишком длинный ответ нейросети или что то другое')

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
