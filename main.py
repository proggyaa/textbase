import textbase
from textbase.message import Message
from textbase import models
import os
import tkinter as tk
from tkinter import simpledialog
from typing import List
from send_message import send_sms
import threading
from record_voice import record_audio

# Load your OpenAI API key
models.OpenAI.api_key = "OpenAi-Key"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI. There are no specific prefixes for responses, so you can ask or talk about anything you like. The AI will respond in a natural, conversational manner. Feel free to start the conversation with any question or topic, and let's have a pleasant chat!
"""

@textbase.chatbot("talking-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Your chatbot logic here
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    if "help_word" not in state:
        # Ask the user for the custom help word using a pop-up dialog box
        root = tk.Tk()
        root.withdraw()  
        
        # Prompt the user for the help word using a pop-up dialog box
        user_help_word = simpledialog.askstring(
            "Custom help word",
            "Before we begin, please provide a custom word that you'd like to use as a help word. This word will stay constant across sessions."
        )
        user_name = simpledialog.askstring(
            "User Name",
            "Before we begin, please enter your name."
        )
        
        root.destroy()

        # Store the user's help word in the state
        state["help_word"] = user_help_word
        state["user_name"] = user_name
            
    lastMessage = message_history.pop().content
    
    if state["help_word"].lower() == lastMessage.lower():
        state["help_mode_activated"] = 1
        bot_response = "You triggered the help function! Please enter your current location"
        return bot_response, state

    if "help_mode_activated" in state and state["help_mode_activated"]:
        state["help_mode_activated"] = 0

        # Starts recording that can be used as proof
        recording_thread = threading.Thread(target=record_audio)
        recording_thread.start()

        # Frame message to send to emergency service for help
        location = lastMessage
        info_to_frame_help_message = f"Please frame a message to send to emergency services for domestic abuse. My name is {state['user_name']} I am at location {location} I need urgent help. frame a small urgent message i can send to emergeny services immediately by copy pasting"
        response = models.OpenAI.generate(
        system_prompt=info_to_frame_help_message,
        message_history = [],
        model="gpt-3.5-turbo")
        bot_response = response.strip()
        send_sms(bot_response)

        # immediately also tell user what to do how to defend themselves
        frame_defense_tech = "Where can I hit in self defense that'll disorient the attacker quick and emergency help"
        response = models.OpenAI.generate(
        system_prompt=frame_defense_tech,
        message_history = [],
        model="gpt-3.5-turbo")
        bot_response = "A message for help has been sent to emergency services." + response 
        return bot_response, state
        
    # Generate GPT-3.5 Turbo response
    response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )
    
    bot_response = response.strip()

    return bot_response, state
