# import openai
from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()




my_assistant = client.beta.assistants.retrieve("asst_zh9yfaosMs5SuB3cGmK8PcRM")

st.write(my_assistant)
thread = client.beta.threads.create()
st.write(thread)

thread_message = client.beta.threads.messages.create(
    thread.id,
    role="user",
    content="How many prime numbers are there under 100?"
)

st.write(thread_message)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=my_assistant.id
)
st.write(run)

import time

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run
run = wait_on_run(run, thread)
st.write(run)

messages = client.beta.threads.messages.list(thread_id=thread.id)
st.write(messages)
# thread_message = client.beta.threads.messages.create()
# openai.api_key = "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"  # Replace with your OpenAI API key

# # Function to call the GPT-3 model to categorize the statement
# def categorize_statement(statement):
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Use the appropriate GPT-3 engine
#         prompt=f"Categorize the statement: '{statement}' into one of the predefined categories: Category A, Category B, Category C.",
#         max_tokens=100
#     )
#     return response.choices[0].text.strip()

# # Streamlit app layout
# st.header('This is my header')
# st.title('GPT-3 Chatbot Categorization App')
# statement = st.text_input('Enter a statement:')
# if st.button('Assign Category with GPT-3'):
#     assigned_category = categorize_statement(statement)
#     st.write(f"The statement '{statement}' belongs to {assigned_category}")

# assistant = client.beta.assistants.create(
#     name="Indicator Bot"
#     instructions="You are categorizing english statements based on their semantic meanings. Use the provided documents for the category fields and definitions to inform your categorizations. Only provide categories that are provided in the support documentation. Give short answers.",
#     tools=[{"type": "Retrieval"}],
#     model="gpt-3.5-turbo-0125"
    
# )
# thread = client.beta.threads.create()

# message = client.beta.threads.messages.create(
#     thread_id = thread.id,
#     role="user",
    
# )
st.title('This is the title')


# Set OpenAI API key
# openai.api_key = os.environ.

# Function to interact with GPT-3
# def chat_with_gpt(message):
#     response = openai.Completion.create(
#         engine="davinci",  # GPT-3 model
#         prompt=message,
#         max_tokens=50  # Maximum number of tokens in the response
#     )
#     return response.choices[0].text.strip()

# # Streamlit app
# def main():
#     st.title("Chat with GPT Assistant")
    
#     # Text area for user to input message
#     user_input = st.text_area("You:", "")
    
#     # Button to send message
#     if st.button("Send"):
#         if user_input:
#             # Display user message
#             st.text_area("You:", user_input, disabled=True)
            
#             # Get response from GPT-3
#             response = chat_with_gpt(user_input)
            
#             # Display GPT response
#             st.text_area("GPT-3:", response, disabled=True)
#         else:
#             st.warning("Please enter a message.")

# if __name__ == "__main__":
#     main()