import logging
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# আপনার তৈরি করা বট টোকেন
BOT_TOKEN = "8686312605:AAFe7F7yYtJPTBgsP1Z2bFlBBpoDLPuMDL4"

def fetch_market_signal(ticker_symbol="BTC-USD"):
    try:
        data = yf.download(tickers=ticker_symbol, period="1d", interval="5m", progress=False)
        if data.empty:
            return "মার্কেট ডাটা পাওয়া যায়নি।"
        
        data['RSI'] = ta.rsi(data['Close'], length=14)
        latest_rsi = data['RSI'].iloc[-1]
        latest_price = data['Close'].iloc[-1]
        
        response = f"📊 **টিকার:** {ticker_symbol}\n"
        response += f"💰 **বর্তমান মূল্য:** ${latest_price:.2f}\n"
        response += f"📈 **RSI ইন্ডিকেটর:** {latest_rsi:.2f}\n\n"
        
        if latest_rsi < 35:
            response += "🚀 **সিগন্যাল: UP (BUY)**\n*মার্কেট বর্তমানে ওভারসোল্ড, ওপরে ওঠার সম্ভাবনা আছে!*"
        elif latest_rsi > 65:
            response += "🔻 **সিগন্যাল: DOWN (SELL)**\n*মার্কেট বর্তমানে ওভারবট, নিচে নামার সম্ভাবনা আছে!*"
        else:
            response += "⚖️ **সিগন্যাল: HOLD (অপেক্ষা করুন)**\n*মার্কেট এখন স্থিতিশীল, নতুন এন্ট্রি না নেওয়াই ভালো।*"
            
        return response
    except Exception as e:
        return f"ডাটা প্রসেস করতে সমস্যা হয়েছে: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[KeyboardButton("📈 Get Signal (এক ক্লিকে সিগন্যাল)")] ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "স্বাগতম! নিচের বাটনে ক্লিক করলেই আপনি লাইভ মার্কেট সিগন্যাল পেয়ে যাবেন।",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    if user_text == "📈 Get Signal (এক ক্লিকে সিগন্যাল)":
        await update.message.reply_text("🔄 মার্কেট বিশ্লেষণ করা হচ্ছে, একটু অপেক্ষা করুন...")
        signal_result = fetch_market_signal("BTC-USD")
        await update.message.reply_text(signal_result, parse_mode="Markdown")
    else:
        await update.message.reply_text("দয়া করে নিচের বাটনে ক্লিক করে সিগন্যাল নিন।")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("বট চালু হয়েছে...")
    application.run_polling()

if __name__ == '__main__':
    main()
