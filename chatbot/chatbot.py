from openai import ChatCompletion
import openai

def get_chatbot_response(user_message, conversation, preprompt=None):
    # Define your chatbot's predefined prompts
    prompts = conversation.copy()

    # Append preprompt if provided
    if preprompt:
        prompts.append({"role": "assistant", "content": preprompt})

    # Append user input to the conversation
    prompts.append({"role": "user", "content": user_message})

    # Set up and invoke the ChatGPT model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompts,
        api_key="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"
    )

    # Extract chatbot replies from the response
    chatbot_replies = [message['message']['content'] for message in response['choices'] if message['message']['role'] == 'assistant']

    return chatbot_replies
