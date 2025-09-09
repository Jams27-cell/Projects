"""
Simple AI Voice Assistant
A beginner-friendly voice assistant that listens to commands and responds with voice output.
Author: James
Date: 2025
"""

import speech_recognition as sr
import pyttsx3
import datetime
import random
import webbrowser
import sys

class VoiceAssistant:
    """Main Voice Assistant class that handles all operations"""
    
    def __init__(self):
        """Initialize the voice assistant with speech recognition and text-to-speech engines"""
        # Initialize the recognizer for speech input
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize microphone (will be None if not available)
        self.microphone = None
        try:
            self.microphone = sr.Microphone()
            print("✓ Microphone initialized successfully!")
        except:
            print("⚠ No microphone found. You can still use text input.")
        
        # Store assistant name and wake word
        self.name = "Assistant"
        self.is_running = True
        
    def setup_voice(self):
        """Configure voice settings for text-to-speech"""
        # Get available voices
        voices = self.engine.getProperty('voices')
        
        # Set voice (0 for male, 1 for female if available)
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)  # Try female voice
        
        # Set speech rate (words per minute)
        self.engine.setProperty('rate', 180)
        
        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)
    
    def speak(self, text):
        """Convert text to speech and speak it out loud"""
        print(f"🤖 {self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Listen to microphone input and convert speech to text"""
        if not self.microphone:
            return None
            
        with self.microphone as source:
            print("\n🎤 Listening...")
            
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("🔄 Processing speech...")
                
                # Recognize speech using Google's speech recognition
                text = self.recognizer.recognize_google(audio)
                print(f"👤 You said: {text}")
                return text.lower()
                
            except sr.WaitTimeoutError:
                print("⏱ No speech detected (timeout)")
                return None
            except sr.UnknownValueError:
                print("❓ Sorry, I couldn't understand that")
                return None
            except sr.RequestError as e:
                print(f"❌ Error with speech recognition service: {e}")
                return None
    
    def get_text_input(self):
        """Fallback method to get text input from keyboard"""
        try:
            user_input = input("\n💬 Type your command (or 'quit' to exit): ").strip()
            return user_input.lower() if user_input else None
        except KeyboardInterrupt:
            return "quit"
    
    def process_command(self, command):
        """Process the command and generate appropriate response"""
        if not command:
            return
        
        # Convert command to lowercase for easier matching
        command = command.lower()
        
        # === GREETINGS ===
        if any(word in command for word in ['hi', 'hello', 'hey', 'greetings']):
            responses = [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Hey! Nice to hear from you. How can I assist?",
                "Greetings! I'm here to help."
            ]
            self.speak(random.choice(responses))
        
        # === CASUAL CONVERSATION ===
        elif any(phrase in command for phrase in ["what's up", "whats up", "how are you", "how you doing"]):
            responses = [
                "I'm doing great! Just here ready to help you out.",
                "All good here! What would you like to do today?",
                "I'm functioning perfectly! How can I assist you?",
                "Everything's running smoothly! What's on your mind?"
            ]
            self.speak(random.choice(responses))
        
        # === TIME AND DATE ===
        elif any(word in command for word in ['time', 'clock']):
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {current_time}")
        
        elif any(word in command for word in ['date', 'day', 'today']):
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            day_name = datetime.datetime.now().strftime("%A")
            self.speak(f"Today is {day_name}, {current_date}")
        
        # === FIND NEARBY PLACES ===
        elif 'find' in command and any(word in command for word in ['cafe', 'café', 'coffee']):
            self.speak("I'll search for nearby cafés for you.")
            webbrowser.open("https://www.google.com/maps/search/cafe+near+me")
        
        elif 'find' in command and any(word in command for word in ['shop', 'store', 'market']):
            self.speak("Let me find shops near you.")
            webbrowser.open("https://www.google.com/maps/search/shops+near+me")
        
        elif 'find' in command and any(word in command for word in ['restaurant', 'food', 'eat']):
            self.speak("I'll look for restaurants nearby.")
            webbrowser.open("https://www.google.com/maps/search/restaurants+near+me")
        
        # === ASSISTANT INFO ===
        elif any(phrase in command for phrase in ['your name', 'who are you', 'what are you']):
            self.speak(f"I'm {self.name}, your personal voice assistant. I can help you with various tasks!")
        
        elif any(word in command for word in ['help', 'commands', 'what can you do']):
            help_text = """I can help you with several things:
            - Greet you when you say hello
            - Tell you the current time or date
            - Find nearby cafés, shops, or restaurants
            - Have casual conversations
            - And more! Just ask me something."""
            self.speak(help_text)
        
        # === THANK YOU ===
        elif any(word in command for word in ['thank', 'thanks']):
            responses = [
                "You're welcome! Happy to help.",
                "My pleasure! Anything else?",
                "Glad I could help!",
                "Anytime! That's what I'm here for."
            ]
            self.speak(random.choice(responses))
        
        # === GOODBYE ===
        elif any(word in command for word in ['bye', 'goodbye', 'quit', 'exit', 'stop']):
            self.speak("Goodbye! Have a great day!")
            self.is_running = False
        
        # === UNKNOWN COMMAND ===
        else:
            self.speak("I'm not sure how to help with that. Try asking me about the time, or to find nearby places!")
    
    def run(self):
        """Main loop to run the voice assistant"""
        # Welcome message
        self.speak("Hello! I'm your voice assistant. How can I help you today?")
        
        # Determine input mode
        use_voice = self.microphone is not None
        
        if not use_voice:
            print("\n📝 Voice input not available. Using text input mode.")
            self.speak("Voice input is not available, so please type your commands.")
        
        # Main interaction loop
        while self.is_running:
            try:
                # Get user input (voice or text)
                if use_voice:
                    # Try voice first
                    user_input = self.listen()
                    
                    # If voice didn't work, offer text input
                    if user_input is None:
                        print("💡 Tip: You can also type your command if voice isn't working.")
                        user_input = self.get_text_input()
                else:
                    # Text-only mode
                    user_input = self.get_text_input()
                
                # Process the command
                if user_input:
                    self.process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n\n⚠ Interrupted by user")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                self.speak("Sorry, I encountered an error. Please try again.")

def main():
    """Main function to start the voice assistant"""
    print("""
    ╔════════════════════════════════════╗
    ║   🤖 AI VOICE ASSISTANT 🤖         ║
    ║   Simple & Expandable              ║
    ╚════════════════════════════════════╝
    """)
    
    # Create and run the assistant
    assistant = VoiceAssistant()
    
    try:
        assistant.run()
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        print("\n👋 Thanks for using the Voice Assistant!")

if __name__ == "__main__":

    main()
