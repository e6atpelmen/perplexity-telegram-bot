# perplexity-telegram-bot
Telegram bot with Perplexity AI integration supporting multiple models

## Описание

Телеграм-бот с интеграцией Perplexity AI, поддерживающий несколько моделей искусственного интеллекта.

## Возможности

- Выбор из 7 моделей AI (Sonar, GPT-5.1, Claude Opus 4.5, Gemini 3 Pro, Grok 4.1, Мышление Kimi K2, Claude Sonnet 4.5)
- Хранение контекста диалога для каждого пользователя
- Удобное меню с кнопками управления
- Команды: /start, /help, /reset

## Установка и деплой на Render

### 1. Получение токенов

**Telegram Bot Token:**
1. Напишите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям и сохраните полученный токен

**Perplexity API Key:**
1. Зайдите на https://www.perplexity.ai/settings/api
2. Создайте новый API ключ
3. Скопируйте ключ

### 2. Деплой на Render

1. Зайдите на https://render.com и войдите в аккаунт
2. Нажмите "New" → "Background Worker"
3. Подключите этот GitHub репозиторий
4. Настройте параметры:
   - **Name**: perplexity-telegram-bot
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
5. Добавьте переменные окружения:
   - `BOT_TOKEN` = ваш токен от BotFather
   - `PERPLEXITY_API_KEY` = ваш API ключ Perplexity
6. Нажмите "Create Background Worker"

Бот автоматически запустится и будет работать 24/7.

## Изменение приветственного текста

Откройте файл `bot.py` и найдите функцию `start()`. Измените текст в переменных:
- `welcome_text` - основное приветствие
- `instructions_text` - инструкции по использованию
- `model_info_text` - описание моделей

## Изменение маппинга моделей

В файле `bot.py` найдите словарь `MODEL_MAPPING`. Измените значения для нужных моделей:

```python
MODEL_MAPPING = {
    "Sonar": "llama-3.1-sonar-large-128k-online",
    "GPT-5.1": "llama-3.1-sonar-large-128k-online",
    # ... остальные модели
}
```
