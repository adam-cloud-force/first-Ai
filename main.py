#!/usr/bin/env python3
"""
🤖 Personal AI Assistant for Basic Needs
Created for learning AI engineering concepts!

This AI assistant demonstrates key concepts in AI engineering:
1. Natural Language Processing (NLP)
2. API integration
3. Local AI models
4. Conversation handling
5. Modular design patterns

Author: Future AI Engineer (Age 13!)
"""

import os
import sys
import json
import datetime
import re
from typing import Dict, List, Any, Optional

# Third-party imports
try:
    import requests
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    import pyttsx3  # Text-to-speech
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

class AIAssistant:
    """
    🧠 Our Main AI Assistant Class
    
    This is the "brain" of our AI. In AI engineering, we often use classes
    to organize our code and keep track of the AI's "state" (what it knows
    and remembers).
    
    Key AI Concepts Demonstrated:
    - State Management: The AI remembers conversation history
    - Intent Recognition: Understanding what the user wants
    - Response Generation: Creating appropriate responses
    - Modularity: Breaking complex tasks into smaller functions
    """
    
    def __init__(self, name: str = "ALEX"):
        """
        🏗️ Initialize our AI Assistant
        
        This is called when we create a new AI assistant.
        We set up all the basic properties and capabilities.
        """
        self.name = name
        self.console = Console()  # For pretty terminal output
        self.conversation_history = []  # Memory of our conversation
        self.user_preferences = {}  # What we learn about the user
        self.capabilities = [
            "basic_conversation",
            "math_calculations", 
            "weather_lookup",
            "web_search",
            "reminders",
            "time_queries",
            "learning_assistant"
        ]
        
        # Initialize text-to-speech (optional)
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_enabled = True
            # Set speech rate (words per minute)
            self.tts_engine.setProperty('rate', 150)
        except:
            self.tts_enabled = False
            
        self.console.print(f"🤖 {self.name} AI Assistant initialized!")
        self.console.print("Type 'help' to see what I can do, or 'quit' to exit.")
    
    def speak(self, text: str):
        """
        🔊 Text-to-Speech Function
        
        This demonstrates how AI assistants can have multiple output modes.
        Not just text, but also voice!
        """
        if self.tts_enabled:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass  # Fail silently if speech doesn't work
    
    def recognize_intent(self, user_input: str) -> str:
        """
        🎯 Intent Recognition - A Core AI Concept!
        
        This function tries to understand what the user wants to do.
        In more advanced AI systems, this might use machine learning models,
        but we're starting with rule-based matching.
        
        Intent recognition is crucial in AI because:
        - It helps the AI understand user goals
        - It routes requests to the right functions
        - It enables more natural conversations
        """
        user_input = user_input.lower().strip()
        
        # Math operations
        if any(word in user_input for word in ['calculate', 'math', '+', '-', '*', '/', 'equals']):
            return 'math'
        
        # Weather queries
        if any(word in user_input for word in ['weather', 'temperature', 'forecast', 'rain', 'sunny']):
            return 'weather'
        
        # Web search
        if any(word in user_input for word in ['search', 'look up', 'find information', 'google']):
            return 'web_search'
        
        # Time queries
        if any(word in user_input for word in ['time', 'date', 'what day', 'when']):
            return 'time'
        
        # Reminders
        if any(word in user_input for word in ['remind', 'remember', 'note', 'todo']):
            return 'reminder'
        
        # Learning assistance
        if any(word in user_input for word in ['explain', 'teach', 'learn', 'how does', 'what is']):
            return 'learning'
        
        # Help
        if any(word in user_input for word in ['help', 'commands', 'what can you do']):
            return 'help'
        
        # Default to conversation
        return 'conversation'
    
    def handle_math(self, user_input: str) -> str:
        """
        🧮 Calculator Function
        
        This demonstrates how AI can process and solve problems.
        We're using regular expressions (regex) to find math expressions.
        """
        try:
            # Extract mathematical expressions
            math_pattern = r'[\d+\-*/().\s]+'
            expressions = re.findall(math_pattern, user_input)
            
            if expressions:
                expression = expressions[0].strip()
                # Safety: only allow basic math operations
                allowed_chars = set('0123456789+-*/(). ')
                if all(c in allowed_chars for c in expression):
                    result = eval(expression)
                    return f"🧮 {expression} = {result}"
            
            return "🤔 I couldn't find a math expression to calculate. Try something like '5 + 3' or 'calculate 10 * 7'"
        
        except Exception as e:
            return f"❌ Math error: {str(e)}"
    
    def handle_weather(self, user_input: str) -> str:
        """
        🌤️ Weather Function
        
        This demonstrates API integration - a crucial skill in AI engineering!
        Real AI systems often need to fetch data from external sources.
        
        Note: For this example, we'll simulate weather data.
        In a real app, you'd use APIs like OpenWeatherMap.
        """
        # Extract location if mentioned
        location = "your location"
        if "in" in user_input:
            parts = user_input.split("in")
            if len(parts) > 1:
                location = parts[-1].strip()
        
        # Simulated weather data (in a real app, you'd call an API)
        import random
        temperatures = [68, 72, 75, 78, 82, 85]
        conditions = ["sunny", "partly cloudy", "cloudy", "rainy"]
        
        temp = random.choice(temperatures)
        condition = random.choice(conditions)
        
        return f"🌤️ The weather in {location} is {temp}°F and {condition}.\n💡 AI Learning Note: This uses simulated data. Real weather apps use APIs like OpenWeatherMap!"
    
    def handle_web_search(self, user_input: str) -> str:
        """
        🔍 Web Search Function
        
        This shows how AI can access external information.
        We'll use Wikipedia as a simple knowledge source.
        """
        try:
            import wikipedia
            
            # Extract search query
            query = user_input.replace("search", "").replace("look up", "").replace("find information about", "").strip()
            
            if not query:
                return "🔍 What would you like me to search for?"
            
            # Search Wikipedia
            summary = wikipedia.summary(query, sentences=2)
            return f"🔍 Here's what I found about '{query}':\n\n{summary}\n\n💡 Source: Wikipedia"
        
        except wikipedia.exceptions.DisambiguationError as e:
            return f"🔍 Multiple results found for '{query}'. Try being more specific. Options: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return f"🔍 I couldn't find information about '{query}'. Try a different search term."
        except Exception as e:
            return f"🔍 Search error: {str(e)}"
    
    def handle_time(self, user_input: str) -> str:
        """
        ⏰ Time and Date Functions
        """
        now = datetime.datetime.now()
        
        if "time" in user_input:
            return f"⏰ Current time: {now.strftime('%I:%M %p')}"
        elif "date" in user_input:
            return f"📅 Today's date: {now.strftime('%A, %B %d, %Y')}"
        else:
            return f"⏰ {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}"
    
    def handle_reminder(self, user_input: str) -> str:
        """
        📝 Simple Reminder System
        
        This demonstrates data persistence - storing information between sessions.
        """
        reminder_file = "/workspace/reminders.json"
        
        try:
            # Load existing reminders
            if os.path.exists(reminder_file):
                with open(reminder_file, 'r') as f:
                    reminders = json.load(f)
            else:
                reminders = []
            
            # Extract reminder text
            reminder_text = user_input.replace("remind me", "").replace("remember", "").strip()
            
            if reminder_text:
                reminder = {
                    "text": reminder_text,
                    "created": datetime.datetime.now().isoformat(),
                    "id": len(reminders) + 1
                }
                reminders.append(reminder)
                
                # Save reminders
                with open(reminder_file, 'w') as f:
                    json.dump(reminders, f, indent=2)
                
                return f"📝 I'll remember: {reminder_text}"
            else:
                # Show existing reminders
                if reminders:
                    reminder_list = "\n".join([f"{r['id']}. {r['text']}" for r in reminders])
                    return f"📝 Your reminders:\n{reminder_list}"
                else:
                    return "📝 You don't have any reminders yet."
        
        except Exception as e:
            return f"📝 Reminder error: {str(e)}"
    
    def handle_learning(self, user_input: str) -> str:
        """
        🎓 Learning Assistant
        
        This function helps explain AI and programming concepts!
        """
        query = user_input.lower()
        
        if "artificial intelligence" in query or "ai" in query:
            return """🧠 Artificial Intelligence (AI) Explained:

AI is like teaching computers to think and learn like humans! Here are the key concepts:

1. **Machine Learning**: Teaching computers to learn from data
2. **Neural Networks**: Computer systems inspired by how our brains work
3. **Natural Language Processing**: Helping computers understand human language
4. **Computer Vision**: Teaching computers to "see" and understand images

🚀 Career Path: Start with Python programming, learn math (especially statistics), and practice building projects like this one!"""
        
        elif "machine learning" in query:
            return """🤖 Machine Learning Explained:

Machine Learning is a way to teach computers to make predictions or decisions by learning from examples (data).

**Types of Machine Learning:**
1. **Supervised Learning**: Learning from examples with correct answers
2. **Unsupervised Learning**: Finding patterns in data without answers
3. **Reinforcement Learning**: Learning through trial and error (like playing games)

**Example**: Teaching a computer to recognize cats in photos by showing it thousands of cat pictures!"""
        
        elif "programming" in query or "code" in query:
            return """💻 Programming for AI:

**Essential Languages:**
1. **Python** - Most popular for AI (what we're using now!)
2. **R** - Great for data science
3. **JavaScript** - For web-based AI applications

**Key Skills to Learn:**
- Variables and functions
- Data structures (lists, dictionaries)
- Libraries and APIs
- Problem-solving thinking

**Practice Tip**: Build small projects like this AI assistant to learn by doing!"""
        
        else:
            return "🎓 I can explain AI concepts, machine learning, programming, and more! Ask me about any of these topics."
    
    def handle_conversation(self, user_input: str) -> str:
        """
        💬 Basic Conversation Handler
        
        This is where we handle general chat and build rapport with the user.
        """
        user_input = user_input.lower()
        
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        goodbyes = ["bye", "goodbye", "see you", "exit", "quit"]
        
        if any(greeting in user_input for greeting in greetings):
            return f"👋 Hello! I'm {self.name}, your AI assistant. I'm here to help with basic tasks and teach you about AI engineering!"
        
        elif any(goodbye in user_input for goodbye in goodbyes):
            return "👋 Goodbye! Keep learning and building amazing things! 🚀"
        
        elif "how are you" in user_input:
            return "🤖 I'm running smoothly and ready to help! How can I assist you today?"
        
        elif "thank you" in user_input or "thanks" in user_input:
            return "😊 You're welcome! I'm here to help you learn and grow as an AI engineer!"
        
        else:
            return "🤔 I'm not sure how to respond to that. Try asking me to calculate something, search for information, or explain AI concepts!"
    
    def show_help(self) -> str:
        """
        ❓ Help Function - Shows what the AI can do
        """
        help_text = f"""
🤖 {self.name} AI Assistant - Command Guide

📋 **What I Can Do:**

🧮 **Math & Calculations**
   • "calculate 5 + 3"
   • "what's 15 * 8?"

🌤️ **Weather** (simulated)
   • "what's the weather?"
   • "weather in New York"

🔍 **Web Search** (Wikipedia)
   • "search for Python programming"
   • "look up artificial intelligence"

⏰ **Time & Date**
   • "what time is it?"
   • "what's today's date?"

📝 **Reminders**
   • "remind me to study Python"
   • "show my reminders"

🎓 **Learning Assistant**
   • "explain artificial intelligence"
   • "teach me about machine learning"
   • "what is programming?"

💬 **General Conversation**
   • Just chat with me naturally!

🎯 **Commands:**
   • "help" - Show this menu
   • "quit" - Exit the program

💡 **Learning Tip:** Try different commands and see how the AI recognizes your intent!
"""
        return help_text
    
    def process_input(self, user_input: str) -> str:
        """
        🔄 Main Processing Function
        
        This is the "brain center" that:
        1. Recognizes what the user wants (intent)
        2. Routes to the appropriate function
        3. Returns the response
        
        This pattern is used in most AI systems!
        """
        # Store conversation history
        self.conversation_history.append({
            "user": user_input,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Recognize intent and route to appropriate handler
        intent = self.recognize_intent(user_input)
        
        if intent == 'math':
            response = self.handle_math(user_input)
        elif intent == 'weather':
            response = self.handle_weather(user_input)
        elif intent == 'web_search':
            response = self.handle_web_search(user_input)
        elif intent == 'time':
            response = self.handle_time(user_input)
        elif intent == 'reminder':
            response = self.handle_reminder(user_input)
        elif intent == 'learning':
            response = self.handle_learning(user_input)
        elif intent == 'help':
            response = self.show_help()
        else:
            response = self.handle_conversation(user_input)
        
        # Store AI response in history
        self.conversation_history.append({
            "ai": response,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        return response
    
    def run(self):
        """
        🚀 Main Program Loop
        
        This keeps the AI running and responsive to user input.
        """
        self.console.print(Panel.fit(
            f"🤖 Welcome to {self.name} - Your Personal AI Assistant!\n"
            "🎓 Built for learning AI engineering concepts\n"
            "💡 Type 'help' to see what I can do",
            title="AI Assistant",
            border_style="blue"
        ))
        
        while True:
            try:
                # Get user input
                user_input = input(f"\n🙋 You: ").strip()
                
                # Check for quit command
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self.console.print("👋 Thanks for learning with me! Keep building amazing AI projects! 🚀")
                    break
                
                if not user_input:
                    continue
                
                # Process input and get response
                response = self.process_input(user_input)
                
                # Display response with nice formatting
                self.console.print(f"🤖 {self.name}: {response}")
                
                # Optional: speak the response
                if len(response) < 200:  # Only speak shorter responses
                    self.speak(response.replace("🤖", "").replace("💡", "").replace("🔍", ""))
                
            except KeyboardInterrupt:
                self.console.print("\n👋 Goodbye! Keep learning! 🚀")
                break
            except Exception as e:
                self.console.print(f"❌ Error: {str(e)}")

def main():
    """
    🎯 Main Function - Entry point of our program
    """
    print("🔧 Initializing AI Assistant...")
    
    # Create and run the AI assistant
    ai = AIAssistant("ALEX")
    ai.run()

if __name__ == "__main__":
    main()