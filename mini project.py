import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import datetime
import os
import random
import requests
import smtplib

engine = pyttsx3.init()
engine.setProperty('rate', 170)  
engine.setProperty('volume', 1.0)  

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def listen():
    """Capture and return the user's voice command."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you repeat?")
        return ""
    except sr.RequestError:
        speak("Could not request results, check your internet connection.")
        return ""

def open_youtube():
    """Open YouTube in a web browser."""
    speak("Opening YouTube")
    webbrowser.open("https://www.youtube.com")

def search_youtube(query):
    """Search for a specific video on YouTube."""
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    speak(f"Searching YouTube for {query}")
    webbrowser.open(url)

def get_time():
    """Tell the current time."""
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}")

def get_weather(city="India"):
    """Fetch and speak the weather details of a given city."""
    API_KEY = "your_openweathermap_api_key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(base_url).json()
        temp = response['main']['temp']
        weather_desc = response['weather'][0]['description']
        speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
    except:
        speak("Sorry, I couldn't fetch the weather. Please check your internet connection.")

def play_music(music_dir="C:/Users/nm484/Music/favorite songs"):
    """Play a random music file from the specified directory."""
    try:
        songs = [song for song in os.listdir(music_dir) if song.endswith('.mp3')]
        if songs:
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            speak(f"Playing {song}")
        else:
            speak("No music files found in the directory.")
    except:
        speak("Music directory not found.")

def send_email(to_email, subject, message):
    """Send an email from a Gmail account."""
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_email, email_message)
        server.quit()
        speak("Email sent successfully.")
    except:
        speak("Failed to send email. Check your email credentials or internet connection.")


def search_wikipedia(query):
    """Search Wikipedia and speak the summary."""
    query = query.strip()  

    if not query:
        speak("Please provide a search query.")
        return

    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia, {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"There are multiple results for {query}. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any results on Wikipedia.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")


def open_random_app(apps_list):
    """Open a random application from a given list."""
    if apps_list:
        app = random.choice(apps_list)
        os.startfile(app)
        speak(f"Opening {app}")
    else:
        speak("No applications found in the list.")

def main():
    """Main function to run the assistant."""
    speak("Hello! How can I assist you?")
    while True:
        command = listen()
        
        if "open youtube" in command:
            open_youtube()
        elif "search youtube for" in command:
            search_youtube(command.replace("search youtube for", "").strip())
        elif "what's the time" in command or "tell me the time" in command:
            get_time()
        elif "weather" in command:
            city = command.replace("weather in", "").strip()
            get_weather(city if city else "india")
        elif "play music" in command:
            play_music("C:/Users/nm484/Music/favorite songs")
        elif "send email" in command:
            speak("Who do you want to send an email to?")
            recipient = listen()
            speak("What should be the subject?")
            subject = listen()
            speak("What should I say in the email?")
            message = listen()
            send_email(recipient, subject, message)
        elif "wikipedia" in command:
            search_query = command.replace("wikipedia", "").strip()
            search_wikipedia(search_query)
        elif "open random app" in command:
            apps = ["C:/Program Files/Google/Chrome/Application/chrome.exe",
                    "C:/Windows/System32/notepad.exe",
                    "C:/Windows/System32/calc.exe"]
            open_random_app(apps)
        elif "exit" in command or "quit" in command:
            speak("Goodbye! Have a great day.")
            break
        else:
            speak("Sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
