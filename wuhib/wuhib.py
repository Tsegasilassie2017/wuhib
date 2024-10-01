import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '7446710670:AAH_zeVEooux5tCahvWmVJax1yqz8amk420'  
CHANNEL_ID = '@wuhibconsultancy'  # Use the channel username or chat ID
pending_questions = []
GUIDELINES_FILE_PATH = 'C:/Users/hp/Desktop/wuhib/guidelines/tsega new 2017 BSC.docx'  # Ensure the file path and extension are correct

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username else "there"
    
    logger.info(f"User {username} started the bot.")

    # Keyboard layout
    keyboard = [
        [InlineKeyboardButton("Ask a question", callback_data='ask_question')],
        [InlineKeyboardButton("View pending questions", callback_data='view_pending')],
        [InlineKeyboardButton("Submit a paper for comment", callback_data='submit_a_paper')],
        [InlineKeyboardButton("Books", callback_data='Books')],
        [InlineKeyboardButton("Guidelines", callback_data='guidelines')],
        [InlineKeyboardButton("Help", callback_data='help')],
        [InlineKeyboardButton("About", callback_data='about')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f'Hi {username}, welcome to Wuhib. How can I help you today?',
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    logger.info(f"Button pressed: {query.data}")

    if query.data == 'ask_question':
        await query.edit_message_text("Please enter your question:")
        context.user_data['asking_question'] = True
    elif query.data == 'view_pending':
        if pending_questions:
            pending_text = "\n".join(pending_questions)
            await query.edit_message_text(f"Pending Questions:\n{pending_text}")
        else:
            await query.edit_message_text("No pending questions.")
    elif query.data == 'guidelines':
        logger.info("Attempting to send the guidelines file.")
        try:
            with open(GUIDELINES_FILE_PATH, 'rb') as file:
                await context.bot.send_document(chat_id=query.from_user.id, document=file)
            await query.edit_message_text("Here are the guidelines you requested.")
        except FileNotFoundError:
            logger.error("Guidelines file not found.")
            await query.edit_message_text("Sorry, the guidelines file was not found.")
        except Exception as e:
            logger.error(f"Error sending document: {e}")
            await query.edit_message_text("Sorry, I couldn't send the guidelines.")

async def receive_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('asking_question'):
        question = update.message.text
        pending_questions.append(question)
        logger.info(f"Received question: {question}")
        await update.message.reply_text(f"Thank you for your question: '{question}'")
        context.user_data['asking_question'] = False

async def approve_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if pending_questions:
        question = pending_questions.pop(0)
        await context.bot.send_message(chat_id=CHANNEL_ID, text=f"Approved Question: '{question}'")
        await update.message.reply_text(f"Question approved and sent to the channel: '{question}'")
    else:
        await update.message.reply_text("No pending questions to approve.")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_question))
    application.add_handler(CommandHandler("approve", approve_question))

    application.run_polling()

if __name__ == '__main__':
    main()