import requests
import pyttsx3
import speech_recognition as sr
import pywhatkit
import schedule
import time

# 🔑 API KEY
api_key = "5a1bfebf342dc4e2ac70bfb55234a489"

# 📱 WhatsApp number (country code required)
whatsapp_number = "+923430856239"

# 🔊 Voice engine
engine = pyttsx3.init()

def speak(text):
    print("🤖 Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# 🌦 WEATHER FUNCTION
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        data = requests.get(url).json()

        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]

            msg = f"{city} ka weather {condition} hai, temperature {temp}°C aur humidity {humidity}% hai."
            speak(msg)
            return msg
        else:
            speak("City nahi mili.")
            return None

    except:
        speak("Internet error hai.")
        return None

# 🎤 VOICE INPUT
def voice_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        r.adjust_for_ambient_noise(source)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except:
            return ""

    try:
        command = r.recognize_google(audio)
        print("🗣 You said:", command)
        return command.lower()
    except:
        return ""

# 🧠 CITY EXTRACTION
def extract_city(command):
    ignore_words = [
        "check", "weather", "whether", "the", "in", "of",
        "please", "tell", "me", "what", "is", "today"
    ]

    words = command.split()
    city_words = [w for w in words if w not in ignore_words]

    return city_words[-1].title() if city_words else ""

# 📲 FIXED WHATSAPP FUNCTION
def send_whatsapp(message):
    try:
        print("📲 Sending WhatsApp...")

        pywhatkit.sendwhatmsg_instantly(
            whatsapp_number,
            message,
            wait_time=20,   # 🔥 FIX: page load time
            tab_close=True,
            close_time=5
        )

        speak("WhatsApp message sent.")
    except:
        speak("WhatsApp send failed.")

# ⏰ DAILY WEATHER
def daily_weather():
    city = "Lahore"
    msg = get_weather(city)

    if msg:
        send_whatsapp(msg)

schedule.every().day.at("08:00").do(daily_weather)

# 🚀 START
speak("Weather AI Agent started")

while True:
    schedule.run_pending()

    command = voice_command()

    if command:
        print("DEBUG:", command)

        # 🌦 WEATHER DETECTION
        if "weather" in command or "whether" in command or "weath" in command:

            city = extract_city(command)

            if city:
                speak(f"Checking weather for {city}")
                result = get_weather(city)

                if result:
                    send_whatsapp(result)
            else:
                speak("City detect nahi ho saki")

        elif "stop" in command or "exit" in command:
            speak("System shutting down")
            break

        else:
            speak("Weather command samajh nahi aaya")

    time.sleep(1)