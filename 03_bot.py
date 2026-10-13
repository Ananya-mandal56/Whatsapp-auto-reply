import pyautogui
import time
import pyperclip
import google.generativeai as genai
import os
from datetime import datetime

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyCSmHb1DXWt7FSJ1V8dRzV1kyr3NdTsLkA"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

def setup_model():
    """Initialize and return the Gemini model"""
    try:
        model = genai.GenerativeModel("gemini-pro")
        return model
    except Exception as e:
        print(f"Error setting up model: {str(e)}")
        return None

def is_last_message_from_sender(chat_log, sender_name="Gourav"):
    """Check if the last message is from the specified sender"""
    try:
        messages = chat_log.strip().split("\n")
        for message in reversed(messages):
            if "] " in message:  # Looking for timestamp format
                name = message.split("] ")[1].split(":")[0]
                if name.strip() == sender_name:
                    return True
                else:
                    return False
    except Exception as e:
        print(f"Error checking last message: {str(e)}")
        return False
    return False

def get_chat_history():
    """Select and copy chat history"""
    try:
        # Select chat text
        pyautogui.moveTo(711, 170)
        pyautogui.dragTo(1730, 931, duration=2.0, button='left')
        
        # Copy selected text
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        
        # Reset cursor position
        pyautogui.click(1319, 989)
        
        return pyperclip.paste()
    except Exception as e:
        print(f"Error getting chat history: {str(e)}")
        return None

def send_response(response):
    """Send the AI response to the chat"""
    try:
        # Copy response to clipboard
        pyperclip.copy(response)
        
        # Click message input box and paste
        pyautogui.click(1265, 982)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"Error sending response: {str(e)}")
        return False

def main():
    print("Starting AI Chat Bot...")
    
    # Initial setup
    model = setup_model()
    if not model:
        print("Failed to initialize model. Exiting...")
        return
    
    # Click on the chat window to focus
    pyautogui.click(1358, 1055)
    time.sleep(2)
    
    print("Bot is running. Press Ctrl+C to stop.")
    
    while True:
        try:
            # Wait between checks
            time.sleep(5)
            
            # Get chat history
            chat_history = get_chat_history()
            if not chat_history:
                continue
                
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking messages...")
            
            # Check if last message is from sender
            if is_last_message_from_sender(chat_history):
                print("New message detected from sender!")
                
                # Generate AI response
                prompt = f"""You are a friendly chat assistant. Please respond to this conversation naturally and briefly:
                {chat_history}"""
                
                try:
                    completion = model.generate_content(prompt)
                    response = completion.text
                    print(f"Gourav: {response}")
                    
                    # Send the response
                    if send_response(response):
                        print("Response sent successfully!")
                    else:
                        print("Failed to send response")
                        
                except Exception as e:
                    print(f"Error generating response: {str(e)}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()