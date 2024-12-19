# meta developer: @gemeguardian
# meta name: Gemini
# meta description: Модуль для взаимодействия с моделью Gemini от Google.
# meta version: 1.0.0
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
        "no_api_key": "🚫 Пожалуйста, установите API ключ Google AI в .config этого модуля.",
        "processing": "⏳ Обработка запроса...",
        "error": "🚫 Произошла ошибка при обработке запроса.",
        "no_query": "🚫 Пожалуйста, введите запрос.",
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
        
        try:
            await utils.answer(message, self.strings["processing"])
            genai.configure(api_key=api_key)
            
            # Настройка модели
            generation_config = {
              "temperature": 1,
              "top_p": 0.95,
              "top_k": 64,
              "max_output_tokens": 8192,
            }

            model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config)
            
            response = await utils.run_sync(model.generate_content, args)
            
            await utils.answer(message, response.text)

        except Exception as e:
            await utils.answer(message, f"{self.strings['error']}\n\n<code>{e}</code>")
