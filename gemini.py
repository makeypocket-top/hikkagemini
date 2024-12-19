# meta developer: @gemeguardian
# meta name: Gemini
# meta description: Модуль для взаимодействия с моделью Gemini от Google.
# meta version: 1.0.1
# meta license: GPLv3
# meta command: gm

import os
import google.generativeai as genai
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class GeminiMod(loader.Module):
    """Модуль для взаимодействия с моделью Gemini от Google."""
    strings = {
        "name": "Gemini",
        "no_api_key": "🚫 <b>Пожалуйста, установите API ключ Google AI в .config этого модуля.</b>",
        "processing": "⏳ <b>Обработка запроса...</b>",
        "error": "🚫 <b>Произошла ошибка при обработке запроса.</b>",
        "no_query": "🚫 <b>Пожалуйста, введите запрос.</b>",
        "gemini_api_key": "Ключ API для Google AI Gemini"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "GEMINI_API_KEY",
                "YOUR_API_KEY",
                lambda: self.strings["gemini_api_key"],
                validator=loader.validators.String()
            ),
        )

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(ru_doc="<запрос> - Отправить запрос модели Gemini")
    async def gmcmd(self, message: Message):
        """<запрос> - Отправить запрос модели Gemini"""
        api_key = self.config["GEMINI_API_KEY"]

        if api_key == "YOUR_API_KEY" or not api_key:
            await utils.answer(message, self.strings["no_api_key"])
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_query"])
            return
        
        message = await utils.answer(message, self.strings["processing"])
        
        try:
            genai.configure(api_key=api_key)
            
            # Настройка модели
            generation_config = {
              "temperature": 0.9,
              "top_p": 1,
              "top_k": 1,
              "max_output_tokens": 2048,
            }

            safety_settings = [
              {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
              },
              {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
              },
              {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
              },
              {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
              },
            ]

            model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
            
            response = await utils.run_sync(model.generate_content, args)
            
            await utils.answer(message, response.text)

        except Exception as e:
            await utils.answer(message, f"{self.strings['error']}\n\n<code>{e}</code>")
