import os, logging, requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
BOT_TOKEN = os.getenv('BOT_TOKEN')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

MODEL_MAPPING = {"Sonar": "sonar", "GPT-5.1": "sonar-pro", "Claude Opus 4.5": "sonar-reasoning",
                "Gemini 3 Pro": "sonar", "Grok 4.1": "sonar-pro", "Мышление Kimi K2": "sonar-reasoning-pro",
                "Claude Sonnet 4.5": "sonar-pro"}
user_context = {}

def get_ctx(uid):
    if uid not in user_context: user_context[uid] = {"model": "sonar", "history": []}
    return user_context[uid]

def call_api(model, msgs):
    try:
        r = requests.post("https://api.perplexity.ai/chat/completions",
                        headers={"Authorization": f"Bearer {PERPLEXITY_API_KEY}", "Content-Type": "application/json"},
                        json={"model": model, "messages": msgs}, timeout=60)
        return r.json()['choices'][0]['message']['content'] if r.status_code == 200 else f"❌ Ошибка: {r.status_code}"
    except Exception as e: return f"❌ Ошибка: {e}"

async def start(u, c):
    get_ctx(u.effective_user.id)
    kb = [[InlineKeyboardButton("🔧 Выбрать модель", callback_data='sm')],
          [InlineKeyboardButton("📖 Инструкция", callback_data='h')],
          [InlineKeyboardButton("🗑 Очистить контекст", callback_data='r')]]
    await u.message.reply_text(
        "🐕 *Привет! Я Дохуя умный Барбос!*\n\n"
        "💎 Выбери модель AI для общения:\n"
        "• *Sonar* - поиск в реальном времени\n"
        "• *GPT-5.1* - самая продвинутая модель OpenAI\n"
        "• *Claude Opus 4.5* - лучшее понимание контекста\n"
        "• *Gemini 3 Pro* - мультимодальный AI от Google\n"
        "• *Grok 4.1* - остроумный AI с юмором\n"
        "• *Мышление Kimi K2* - глубокий анализ\n"
        "• *Claude Sonnet 4.5* - быстрые и точные ответы\n\n"
        "📱 *Как пользоваться:*\n"
        "1. Выбери модель кнопкой ниже\n"
        "2. Задай любой вопрос\n"
        "3. Получи умный ответ!\n\n"
        "🔄 /reset - очистить историю\n"
        "📖 /help - показать инструкцию\n"
        "🏠 *Меню* - главное меню",
        parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(kb))

async def btn(u, c):
    q = u.callback_query; await q.answer(); uid = u.effective_user.id; ctx = get_ctx(uid)
    if q.data == 'sm':
        cur = [k for k,v in MODEL_MAPPING.items() if v==ctx['model']][0]
        kb = [[InlineKeyboardButton(f"{'✅ ' if n==cur else ''}{n}", callback_data=f'm_{n}')] for n in MODEL_MAPPING]
        kb.append([InlineKeyboardButton("« Назад", callback_data='mm')])
        await q.edit_message_text(f"🔧 Текущая: *{cur}*", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(kb))
    elif q.data == 'h': await start(u, c)
    elif q.data == 'r':
        ctx['history'] = []; await q.edit_message_text("✅ Контекст очищен!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Меню", callback_data='mm')]]))
    elif q.data == 'mm':
        kb = [[InlineKeyboardButton("🔧 Выбрать модель", callback_data='sm')],
              [InlineKeyboardButton("📖 Инструкция", callback_data='h')],
              [InlineKeyboardButton("🗑 Очистить контекст", callback_data='r')]]
        await q.edit_message_text("🏠 *Меню*", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(kb))
    elif q.data.startswith('m_'):
        name = q.data.replace('m_', ''); ctx['model'] = MODEL_MAPPING[name]
        await q.edit_message_text(f"✅ Модель: *{name}*", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Меню", callback_data='mm')]]))

async def msg(u, c):
    uid = u.effective_user.id; ctx = get_ctx(uid); txt = u.message.text
    ctx['history'].append({"role": "user", "content": txt})
    if len(ctx['history']) > 10: ctx['history'] = ctx['history'][-10:]
    await u.message.chat.send_action("typing")
    resp = call_api(ctx['model'], ctx['history'])
    ctx['history'].append({"role": "assistant", "content": resp})
    await u.message.reply_text(resp)

def main():
    if not BOT_TOKEN or not PERPLEXITY_API_KEY: return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("reset", lambda u,c: get_ctx(u.effective_user.id).update({"history":[]})))
    app.add_handler(CallbackQueryHandler(btn))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg))
    logging.info("🐕 Барбос запущен!")
    app.run_polling()

if __name__ == '__main__': main()
