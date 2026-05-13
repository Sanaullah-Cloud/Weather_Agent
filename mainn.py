import requests
import pywhatkit
import schedule
import time

# 🔑 API KEY
api_key = "5a1bfebf342dc4e2ac70bfb55234a489"

# 📱 WhatsApp number
whatsapp_number = "+923430856239"

# 🌦 Weather function
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        data = requests.get(url).json()

        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]

            message = (
                f"🌦 Daily Weather Update\n"
                f"City: {city}\n"
                f"Condition: {condition}\n"
                f"Temperature: {temp}°C\n"
                f"Humidity: {humidity}%"
            )

            return message
        else:
            return "City not found"

    except:
        return "Weather API error"

# 📲 WhatsApp send
def send_whatsapp(message):
    try:
        pywhatkit.sendwhatmsg_instantly(
            whatsapp_number,
            message,
            wait_time=20,
            tab_close=True,
            close_time=5
        )
        print("✅ WhatsApp message sent")
    except:
        print("❌ WhatsApp send failed")

# ⏰ Daily task (12:06 PM = 12:06)
def daily_task():
    city = "Sargodha"
    msg = get_weather(city)
    send_whatsapp(msg)

# 📅 Schedule time
schedule.every().day.at("12:06").do(daily_task)

print("🚀 Silent Weather Agent Running...")

# 🔁 Infinite loop (no audio, no voice)
while True:
    schedule.run_pending()
    time.sleep(30)