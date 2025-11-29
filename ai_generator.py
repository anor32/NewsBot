from openai import OpenAI
url = "https://www.warhammer-community.com/en-gb/articles/ncmflumo/the-warhammer-community-team-paint-the-heroes-of-warhammer-quest-darkwater/"

class AimlBots:
    model = "tngtech/deepseek-r1t2-chimera:free"
    def generate_news(self,prompt) -> str:
        """отправляет запрос нейросети принимает пользовательский промпт возвращает ответ от бота"""
        api_key = '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'
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
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


