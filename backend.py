import google.generativeai as genai # type: ignore
import os
import sys

try:
    from dotenv import load_dotenv # type: ignore
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv library not found. Ensure GEMINI_API_KEY is set in your environment.")

api_key = os.getenv("Gemini_api")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not set.")
    print("Please set the environment variable or install python-dotenv and create a .env file.")
    sys.exit(1)

try:
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    print("Please ensure your API key is valid and the Generative AI API is enabled for your project.")
    sys.exit(1)

MODEL_NAME = 'gemini-1.5-flash-latest' 

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

generation_config = {
    "temperature": 0.7,         
    "top_p": 1.0,               
    "top_k": 1,                 
    "max_output_tokens": 2048,    
}


def run_chatbot():
    print(f"--- Gemini Chatbot ({MODEL_NAME}) ---")
    print("Type 'quit', 'exit', or 'bye' to end the chat.")
    print("-" * 30)

    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            safety_settings=safety_settings,
            generation_config=generation_config
        )

        chat = model.start_chat(history=[]) 

    except Exception as e:
        print(f"Error initializing the Gemini model: {e}")
        sys.exit(1)


    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("\nChatbot: Goodbye!")
                break

            if not user_input:
                continue 

            response = chat.send_message(user_input)

            print(f"Gemini: {response.text}")

        except KeyboardInterrupt:
            print("\nChatbot: Goodbye! (Interrupted by user)")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            try:
                if response and response.prompt_feedback:
                   print(f"Prompt Feedback: {response.prompt_feedback}")
                if response and response.candidates and response.candidates[0].finish_reason:
                    print(f"Finish Reason: {response.candidates[0].finish_reason}")
                    if response.candidates[0].finish_reason == 'SAFETY':
                       print("Response may have been blocked due to safety settings.")
            except Exception: 
                 pass


if __name__ == "__main__":
    run_chatbot()