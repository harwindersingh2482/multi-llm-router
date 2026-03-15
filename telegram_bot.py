import os
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://multi-llm-router.onrender.com/route"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

user_prompts = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm your Multi-LLM Router Bot!\n\n"
        "Just send me any question and choose which AI model to use!\n\n"
        "⚡ *Fastest* — LLaMA 3.1 8B\n"
        "🧠 *Smartest* — LLaMA 3.3 70B\n"
        "🔥 *Detailed* — Groq Compound\n"
        "📊 *Compare All* — See all 3 at once",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    user_id = update.message.from_user.id
    user_prompts[user_id] = prompt

    keyboard = [
        [
            InlineKeyboardButton("⚡ Fastest", callback_data="fast"),
            InlineKeyboardButton("🧠 Smartest", callback_data="smart"),
        ],
        [
            InlineKeyboardButton("🔥 Detailed", callback_data="detailed"),
            InlineKeyboardButton("📊 Compare All", callback_data="all"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"*Your question:* {prompt}\n\nChoose a model:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    prompt = user_prompts.get(user_id, "No prompt found")
    choice = query.data

    await query.edit_message_text(f"🔄 Processing with {'all models' if choice == 'all' else choice + ' model'}...")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                API_URL,
                json={"prompt": prompt, "max_tokens": 200}
            )
            data = response.json()

        results = data["results"]

        if choice == "fast":
            model_result = next(r for r in results if r["model"] == "llama-3.1-8b-instant")
            reply = f"⚡ *Fastest Model — LLaMA 3.1 8B*\n\n"
            reply += f"💬 {model_result['response'][:500]}\n\n"
            reply += f"⏱ {model_result['latency_seconds']}s | 💰 ${model_result['estimated_cost_usd']}"

        elif choice == "smart":
            model_result = next(r for r in results if r["model"] == "llama-3.3-70b-versatile")
            reply = f"🧠 *Smartest Model — LLaMA 3.3 70B*\n\n"
            reply += f"💬 {model_result['response'][:500]}\n\n"
            reply += f"⏱ {model_result['latency_seconds']}s | 💰 ${model_result['estimated_cost_usd']}"

        elif choice == "detailed":
            model_result = next(r for r in results if r["model"] == "groq/compound")
            reply = f"🔥 *Detailed Model — Groq Compound*\n\n"
            reply += f"💬 {model_result['response'][:500]}\n\n"
            reply += f"⏱ {model_result['latency_seconds']}s | 💰 ${model_result['estimated_cost_usd']}"

        else:
            reply = f"📊 *Comparing All 3 Models*\n\n"
            for result in results:
                reply += f"━━━━━━━━━━━━━━━\n"
                reply += f"🤖 *{result['model']}*\n"
                reply += f"⏱ {result['latency_seconds']}s | 💰 ${result['estimated_cost_usd']}\n"
                reply += f"💬 {result['response'][:200]}\n\n"
            reply += f"━━━━━━━━━━━━━━━\n"
            reply += f"✅ Recommended: `{data['recommended_model']}`"

        await query.edit_message_text(reply[:4000], parse_mode="Markdown")

    except Exception as e:
        await query.edit_message_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_button))
    print("🤖 Bot is running...")
    app.run_polling()