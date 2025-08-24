#!/usr/bin/env python3
"""
🤖 Simple AI Assistant for Learning
No external dependencies required - pure Python!

This demonstrates core AI engineering concepts:
1. Intent Recognition (rule-based)
2. Conversation Handling
3. State Management
4. Modular Design

Author: Future AI Engineer (Age 13!)
"""

import os
import sys
import json
import datetime
import re
import random
import math

class SimpleAI:
    """
    🧠 Simple AI Assistant Class
    
    This teaches fundamental AI concepts without complex dependencies.
    Perfect for understanding the basics before moving to advanced tools!
    
    Core AI Concepts You'll Learn:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. STATE MANAGEMENT: How AI remembers things
    2. INTENT RECOGNITION: Understanding what users want
    3. PATTERN MATCHING: Finding patterns in text
    4. RESPONSE GENERATION: Creating helpful replies
    5. CONVERSATION FLOW: Managing back-and-forth chat
    """
    
    def __init__(self, name="ALEX"):
        """
        🏗️ Initialize the AI Assistant
        
        Think of this as "teaching" the AI its basic knowledge and abilities.
        """
        self.name = name
        self.conversation_memory = []  # Stores our chat history
        self.user_data = {}           # What we learn about the user
        self.knowledge_base = {       # Built-in knowledge
            "ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
            "machine_learning": "Machine Learning is a method of data analysis that automates analytical model building.",
            "python": "Python is a programming language that's great for beginners and AI development!",
            "programming": "Programming is giving instructions to computers to solve problems.",
        }
        
        print(f"🤖 {self.name} Simple AI initialized!")
        print("🎓 Ready to learn AI engineering together!")
        
    def recognize_intent(self, text):
        """
        🎯 Intent Recognition Engine
        
        This is a KEY concept in AI! The AI needs to understand what the user wants.
        We're using rule-based matching (simple but effective for learning).
        
        In real AI systems, this might use:
        - Machine Learning models
        - Neural networks
        - Natural Language Processing libraries
        
        But starting simple helps you understand the fundamentals!
        """
        text = text.lower().strip()
        
        # Mathematics intent
        math_keywords = ['calculate', 'math', '+', '-', '*', '/', 'equals', 'plus', 'minus', 'times', 'divided']
        if any(keyword in text for keyword in math_keywords):
            return 'math'
        
        # Learning intent
        learning_keywords = ['explain', 'what is', 'teach me', 'learn', 'how does', 'tell me about']
        if any(keyword in text for keyword in learning_keywords):
            return 'learning'
        
        # Time intent
        time_keywords = ['time', 'date', 'when', 'today', 'now']
        if any(keyword in text for keyword in time_keywords):
            return 'time'
        
        # Memory intent (saving/retrieving info)
        memory_keywords = ['remember', 'save', 'note', 'recall', 'what did i']
        if any(keyword in text for keyword in memory_keywords):
            return 'memory'
        
        # Game intent
        game_keywords = ['game', 'play', 'fun', 'quiz', 'riddle']
        if any(keyword in text for keyword in game_keywords):
            return 'game'
        
        # Help intent
        help_keywords = ['help', 'commands', 'what can you do', 'capabilities']
        if any(keyword in text for keyword in help_keywords):
            return 'help'
        
        # Default to conversation
        return 'conversation'
    
    def handle_math(self, text):
        """
        🧮 Math Handler - Teaching AI Problem Solving
        
        This shows how AI can parse and solve mathematical problems.
        We use pattern recognition to find numbers and operations.
        """
        try:
            # Simple math patterns
            patterns = [
                r'(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)',  # Addition
                r'(\d+(?:\.\d+)?)\s*\-\s*(\d+(?:\.\d+)?)',  # Subtraction
                r'(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)',  # Multiplication
                r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)',   # Division
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    num1, num2 = float(match.group(1)), float(match.group(2))
                    
                    if '+' in text:
                        result = num1 + num2
                        return f"🧮 {num1} + {num2} = {result}"
                    elif '-' in text:
                        result = num1 - num2
                        return f"🧮 {num1} - {num2} = {result}"
                    elif '*' in text:
                        result = num1 * num2
                        return f"🧮 {num1} × {num2} = {result}"
                    elif '/' in text:
                        if num2 != 0:
                            result = num1 / num2
                            return f"🧮 {num1} ÷ {num2} = {result}"
                        else:
                            return "❌ Cannot divide by zero!"
            
            # If no pattern matched, try to evaluate the whole expression safely
            # Remove words and keep only math characters
            math_expr = re.sub(r'[^0-9+\-*/(). ]', '', text)
            if math_expr.strip():
                try:
                    result = eval(math_expr)
                    return f"🧮 {math_expr.strip()} = {result}"
                except:
                    pass
            
            return "🤔 I couldn't find a math problem to solve. Try something like '5 + 3' or 'calculate 10 * 7'"
            
        except Exception as e:
            return f"❌ Math error: {str(e)}"
    
    def handle_learning(self, text):
        """
        🎓 Learning Handler - AI Teaching Function
        
        This demonstrates how AI can be educational and help users learn!
        """
        text = text.lower()
        
        # Check our knowledge base first
        for topic, info in self.knowledge_base.items():
            if topic in text:
                return f"📚 {info}\n\n💡 Want to learn more? Ask me about specific AI concepts!"
        
        # Specific AI topics
        if 'neural network' in text:
            return """🧠 Neural Networks Explained:

Think of neural networks like a simplified brain! They have:

🔗 NEURONS: Individual processing units (like brain cells)
🔗 LAYERS: Groups of neurons working together
🔗 CONNECTIONS: How information flows between neurons

Example: To recognize a cat in a photo:
1. Input layer receives the image
2. Hidden layers detect features (edges, shapes, patterns)
3. Output layer says "cat" or "not cat"

It's like teaching a computer to think step by step!"""

        elif 'algorithm' in text:
            return """⚙️ Algorithms Explained:

An algorithm is like a recipe for solving problems!

🍰 Recipe Analogy:
1. Ingredients (Input data)
2. Steps (Processing rules)  
3. Final dish (Output result)

🤖 AI Algorithm Example:
1. Give the AI lots of cat photos
2. Teach it to recognize patterns
3. Now it can identify cats in new photos!

Famous AI algorithms: Decision Trees, Random Forest, Neural Networks"""

        elif 'data' in text and 'science' in text:
            return """📊 Data Science Explained:

Data Science is like being a detective with numbers!

🔍 What Data Scientists Do:
1. COLLECT data (like a detective gathering clues)
2. CLEAN data (removing errors and noise)
3. ANALYZE data (finding patterns and insights)
4. PREDICT future outcomes
5. COMMUNICATE findings

🎯 Skills You Need:
- Programming (Python, R)
- Math & Statistics
- Critical thinking
- Curiosity!"""
        
        else:
            return """🎓 I love teaching! I can explain:

🤖 AI FUNDAMENTALS:
• Neural networks
• Machine learning
• Algorithms
• Data science

💻 PROGRAMMING:
• Python basics
• How to code
• Problem solving

Ask me: "Explain neural networks" or "What is an algorithm?"

Remember: The best way to learn AI is by building projects like this one! 🚀"""
    
    def handle_time(self, text):
        """
        ⏰ Time Handler - Basic Information Retrieval
        """
        now = datetime.datetime.now()
        
        if 'time' in text:
            return f"⏰ Current time: {now.strftime('%I:%M %p')}"
        elif 'date' in text:
            return f"📅 Today is: {now.strftime('%A, %B %d, %Y')}"
        else:
            return f"⏰ {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d, %Y')}"
    
    def handle_memory(self, text):
        """
        🧠 Memory Handler - Demonstrates AI State Management
        
        This shows how AI systems can store and retrieve information!
        """
        memory_file = "/workspace/ai_memory.json"
        
        try:
            # Load existing memory
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    memory = json.load(f)
            else:
                memory = {}
            
            if 'remember' in text or 'save' in text:
                # Extract what to remember
                to_remember = text.replace('remember', '').replace('save', '').replace('that', '').strip()
                if to_remember:
                    timestamp = datetime.datetime.now().isoformat()
                    memory[timestamp] = to_remember
                    
                    # Save to file
                    with open(memory_file, 'w') as f:
                        json.dump(memory, f, indent=2)
                    
                    return f"🧠 I'll remember: {to_remember}"
                else:
                    return "🤔 What would you like me to remember?"
            
            else:  # Recall
                if memory:
                    memories = list(memory.values())
                    return f"🧠 Here's what I remember:\n" + "\n".join([f"• {mem}" for mem in memories[-5:]])  # Last 5 memories
                else:
                    return "🧠 I don't have any memories saved yet. Tell me something to remember!"
        
        except Exception as e:
            return f"🧠 Memory error: {str(e)}"
    
    def handle_game(self, text):
        """
        🎮 Game Handler - Making AI Fun and Interactive!
        
        Games help users engage with AI in a fun way.
        """
        games = [
            "🎲 Number Guessing Game: I'm thinking of a number between 1-100. Guess it!",
            "🧩 Riddle: What has keys but no locks, space but no room? (Answer: A keyboard!)",
            "🎯 Math Challenge: Quick! What's 17 × 23?",
            "📝 Word Game: Name 3 things related to AI in 10 seconds!",
            "🤔 Logic Puzzle: If it takes 5 machines 5 minutes to make 5 widgets, how long does it take 100 machines to make 100 widgets?"
        ]
        
        return random.choice(games)
    
    def handle_conversation(self, text):
        """
        💬 Conversation Handler - Natural Language Interaction
        
        This handles general chat and builds rapport with users.
        Building good conversation skills is important for AI assistants!
        """
        text = text.lower()
        
        # Greetings
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        if any(greeting in text for greeting in greetings):
            responses = [
                f"👋 Hello! I'm {self.name}, your AI learning companion!",
                f"🤖 Hi there! Ready to explore AI together?",
                f"😊 Hey! I'm excited to help you learn AI engineering!"
            ]
            return random.choice(responses)
        
        # How are you
        elif 'how are you' in text:
            return "🤖 I'm running perfectly and excited to help you learn! How are you doing with your AI journey?"
        
        # Compliments
        elif any(word in text for word in ['cool', 'awesome', 'amazing', 'great']):
            return "😊 Thank you! AI is pretty amazing, isn't it? What would you like to explore next?"
        
        # Age/creator questions
        elif 'old are you' in text or 'created' in text:
            return "🤖 I was just created today by a brilliant 13-year-old future AI engineer! Pretty cool, right?"
        
        # Default responses
        else:
            responses = [
                "🤔 That's interesting! Tell me more, or ask me about AI concepts!",
                "💭 I'm here to help you learn AI. What would you like to know?",
                "🎓 Let's explore AI together! Try asking me to explain something or solve a math problem.",
                "🚀 Ready for some AI learning? Ask me about neural networks, programming, or anything else!"
            ]
            return random.choice(responses)
    
    def show_help(self):
        """
        ❓ Help System - Shows AI Capabilities
        """
        return f"""
🤖 {self.name} Simple AI Assistant - Learning Edition

🎯 WHAT I CAN DO:

🧮 MATH & CALCULATIONS
   • "calculate 25 + 17"
   • "what's 144 / 12?"
   • "solve 8 * 7"

🎓 LEARNING ASSISTANT  
   • "explain neural networks"
   • "what is machine learning?"
   • "teach me about algorithms"
   • "what is data science?"

⏰ TIME & DATE
   • "what time is it?"
   • "what's today's date?"

🧠 MEMORY SYSTEM
   • "remember I like Python"
   • "what do you remember?"
   • "save that I'm 13 years old"

🎮 GAMES & FUN
   • "let's play a game"
   • "give me a riddle"

💬 GENERAL CHAT
   • Just talk to me naturally!

🔍 CORE AI CONCEPTS DEMONSTRATED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Intent Recognition
✓ Pattern Matching  
✓ State Management
✓ Conversation Flow
✓ Knowledge Retrieval
✓ Response Generation

🚀 NEXT STEPS FOR YOUR AI JOURNEY:
1. Learn Python programming fundamentals
2. Study basic statistics and math
3. Explore machine learning libraries
4. Build more complex AI projects
5. Join AI communities and keep learning!

💡 Type 'quit' to exit anytime.
"""

    def process_input(self, user_input):
        """
        🔄 Main Processing Engine
        
        This is the "brain" of our AI that:
        1. Takes user input
        2. Recognizes intent
        3. Routes to appropriate handler
        4. Returns response
        
        This pattern is fundamental to all AI systems!
        """
        # Save to conversation memory
        self.conversation_memory.append({
            'user': user_input,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        # Recognize what the user wants
        intent = self.recognize_intent(user_input)
        
        # Route to appropriate handler based on intent
        if intent == 'math':
            response = self.handle_math(user_input)
        elif intent == 'learning':
            response = self.handle_learning(user_input)
        elif intent == 'time':
            response = self.handle_time(user_input)
        elif intent == 'memory':
            response = self.handle_memory(user_input)
        elif intent == 'game':
            response = self.handle_game(user_input)
        elif intent == 'help':
            response = self.show_help()
        else:
            response = self.handle_conversation(user_input)
        
        # Save AI response to memory
        self.conversation_memory.append({
            'ai': response,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        return response
    
    def run(self):
        """
        🚀 Main Program Loop
        
        This keeps our AI running and interactive!
        """
        print("\n" + "="*60)
        print(f"🤖 Welcome to {self.name} - Simple AI Assistant!")
        print("🎓 Learn AI Engineering by Building and Using AI!")
        print("💡 Type 'help' to see what I can do")
        print("="*60 + "\n")
        
        while True:
            try:
                # Get user input
                user_input = input(f"🙋 You: ").strip()
                
                # Check for quit
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print(f"\n👋 {self.name}: Thanks for learning with me!")
                    print("🚀 Keep building amazing AI projects!")
                    print("💡 Remember: The best way to learn AI is by doing!")
                    break
                
                if not user_input:
                    continue
                
                # Process input and get response
                response = self.process_input(user_input)
                
                # Display response
                print(f"🤖 {self.name}: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 {self.name}: Goodbye! Keep learning! 🚀")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

def main():
    """
    🎯 Main Function - Entry Point
    """
    print("🔧 Starting Simple AI Assistant...")
    
    # Create and run the AI
    ai = SimpleAI("ALEX")
    ai.run()

if __name__ == "__main__":
    main()