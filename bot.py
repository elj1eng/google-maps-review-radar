import os
import telebot
from dotenv import load_dotenv
from scraper import MapsScraper
from analyzer import ReviewAnalyzer
from main import is_google_maps_responsive

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("Error: TELEGRAM_BOT_TOKEN is not set in .env")
    exit(1)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me a Google Maps place URL, and I will analyze its reviews to find real ratings and fake density.")

@bot.message_handler(func=lambda message: True)
def analyze_url(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "Please provide a valid URL starting with http/https.")
        return
        
    msg = bot.reply_to(message, "🔍 Validating URL...")
    
    if not is_google_maps_responsive(url):
        bot.edit_message_text("❌ Error: The URL provided did not return a valid response.\nEnsure the link is a valid, reachable Google Maps place.", chat_id=msg.chat.id, message_id=msg.message_id)
        return
        
    bot.edit_message_text("🚀 Initializing Scraper... This may take a minute depending on the number of reviews.", chat_id=msg.chat.id, message_id=msg.message_id)
    
    try:
        scraper = MapsScraper(url)
        html_content = scraper.fetch_html()
        
        bot.edit_message_text("⚙️ Analyzing reviews data...", chat_id=msg.chat.id, message_id=msg.message_id)
        
        analyzer = ReviewAnalyzer(html_content)
        summary = analyzer.get_spot_summary()
        report = analyzer.analyze_reviews()
        
        print(summary["name"])
        if not report:
            bot.edit_message_text("⚠️ Analysis failed: No review cards found.", chat_id=msg.chat.id, message_id=msg.message_id)
            return
            
        final_status = "🚨 SUSPICIOUS" if (report['is_fake_h'] or report['is_fake_i']) else "✅ TRUSTWORTHY"
        
        reply_msg = (
            f"{summary['name']}\n\n"
            f"--- SPOT SUMMARY ---\n"
            f"Rating: {summary['rating']} ⭐ | Total Reviews: {summary['total']}\n\n"
            f"--- VERDICT (Sample Size: {report['total_scanned']}) ---\n"
            f"1. Burner Density: {report['h_ratio']*100:.1f}% -> {'⚠️ FAKE' if report['is_fake_h'] else '✅ OK'}\n"
            f"2. Image Density: {report['i_ratio']*100:.1f}% -> {'⚠️ FAKE' if report['is_fake_i'] else '✅ OK'}\n"
            f"3. Real Reviewer Metric (>3 reviews): Avg {report['real_avg_rating']:.2f} ⭐ | Count {report['real_count']} - {report['real_count']/report['total_scanned']*100:.1f}%\n\n"
            f"OVERALL STATUS: {final_status}"
        )
        
        bot.edit_message_text(reply_msg, chat_id=msg.chat.id, message_id=msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"❌ An error occurred during scraping/analysis:\n{str(e)}", chat_id=msg.chat.id, message_id=msg.message_id)

if __name__ == "__main__":
    print("Bot is running... Waiting for messages.")
    bot.infinity_polling()
