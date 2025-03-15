from openai import OpenAI

from app.gpt_chatbot.dao import PromptsDAO


class GptChatBot:
    def __init__(self, api_key: str):
        self._client = self._make_client(api_key)

    @staticmethod
    def _make_client(api_key: str) -> OpenAI:
        client = OpenAI(
            api_key=api_key,
        )

        return client

    async def ask(self, last_messages: list[dict], chatbot_id: int) -> str:
        user_response_data = await self._make_user_response(last_messages, chatbot_id)
        gpt_response_data = self._client.chat.completions.create(**user_response_data)

        try:
            return gpt_response_data.choices[0].message.content
        except IndexError:
            return ''

    async def _make_user_response(self, last_messages: list[dict], chatbot_id: int) -> dict:
        prompt = await self._make_prompt(chatbot_id)

        messages: list[dict] = [prompt]
        messages += last_messages

        response = {
            'model': 'gpt-4o-mini',
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 500
        }

        return response

    @staticmethod
    async def _make_prompt(chatbot_id: int) -> dict:
        prompts = await PromptsDAO().get_prompts(chatbot_id)
        result_prompt = ''

        for prompt in prompts:
            result_prompt += prompt.strip().replace('\n', ' ').replace('  ', ' ')
            result_prompt += ' '

        return {'role': 'system', 'content': result_prompt.strip()}
