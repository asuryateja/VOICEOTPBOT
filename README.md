# VOICEOTPBOT Telegram Bot Documentation

## Introduction

The FastAPI Telegram Bot is a versatile application that enables users to interact with the bot, authenticate themselves, add services, initiate calls with specific service text, and receive OTP input during the call. The application utilizes the FastAPI framework for backend development, the Telegram API for bot interaction, and Twilio for voice call functionality.

## Disclaimer

**ANYONE CAN CHANGE AND USE FREELY.**

This application is provided for educational purposes and experimentation. The developer is not responsible for any illegal or unauthorized usage of this application. Use this application responsibly and according to the laws and regulations of your jurisdiction.


## Prerequisites

Before you begin, ensure you have the following prerequisites in place:

- Twilio Account SID and Auth Token
- Telegram Bot Token
- Python 3 installed
- [FastAPI](https://fastapi.tiangolo.com/) and [Twilio](https://www.twilio.com/docs/libraries/python) Python packages installed
- Access to a Heroku account (for Heroku deployment) or a VPS with SSH access (for VPS deployment)

## Setup

### Telegram Bot Setup

1. **Create a Telegram Bot**: [Create a new Telegram bot](https://core.telegram.org/bots#botfather) and obtain the bot token.

2. **Admin Chat ID**: Find your admin chat ID using a Telegram bot such as [userinfobot](https://telegram.me/userinfobot).

3. **Code Configuration**: Replace `'your_telegram_bot_token'` and `'your_admin_chat_id'` placeholders in the code with the actual values.

### Deploying on Heroku

1. **Heroku Account**: If you don't have one, [create a Heroku account](https://signup.heroku.com/).

2. **Heroku CLI**: Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

3. **Prepare the App**:
   - Initialize a Git repository and commit your code.
   - Create a `requirements.txt` file with your project dependencies.
   - Create a `Procfile` in your project directory and add the following line:
     ```
     web: uvicorn your_app_name:app --host=0.0.0.0 --port=${PORT:-5000}
     ```
     Replace `your_app_name` with your main Python file's name (without the `.py` extension).

4. **Deploy the App**:
   ```sh
   heroku create your-app-name
   git push heroku master
   ```

## Using the Bot

### User Authentication

- **Contact the Admin**: Contact the admin to add your chat ID to the allowed list using the `/addchatid` command.

- **Authenticate Yourself**: Send `/authenticate userid` to the bot to authenticate yourself.

### Adding Services

- **Add a Service**: Use `/addService '<text>' '<service_name>'` to add a new service with a text description.

### Initiating Calls

- **Initiate a Call**: Use `/call <phone_number> <service_name> <otp_digits>` to initiate a call with a specific service's text.

- **Enter OTP**: During the call, you will be prompted to enter the OTP.

## Disclaimer Reminder

Please remember that this application is intended for educational purposes only. Use this application responsibly and adhere to the laws and regulations of your jurisdiction. The developer is not responsible for any misuse of this application.
