import os

from openai import OpenAI

class AimlBots:
    model = "x-ai/grok-4.1-fast:free"
    api_key = os.getenv('OPENAI_API_KEY')
    def generate_news(self,prompt:str) -> str:
        """отправляет запрос нейросети принимает пользовательский промпт возвращает ответ от бота"""

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )


        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt

                },
            ],
         )
        return response.choices[0].message.content


