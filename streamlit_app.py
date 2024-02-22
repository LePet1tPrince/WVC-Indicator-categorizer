# import openai
from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
import time


load_dotenv()

client = OpenAI()


st.header('Indicator Codification App')
with st.expander('About this App'):
    st.write("This app is built using the GPT API. It references the crowdsourcing guide as it's basis of information. Select a category to tag and paste an indicator statement")

my_assistant = client.beta.assistants.retrieve("asst_zh9yfaosMs5SuB3cGmK8PcRM")

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(my_assistant.id, thread, user_input)
    return thread, run


# Emulating concurrent user requests
category_list = ['ALL','Unit of Analysis','Age Group Type','Sector/Cross-cutting Theme','Sub-sector']
selected_category = st.selectbox('Category By',category_list)
indicator_statement = st.text_input('Statement')

submit_button = st.button('Categorize')



# Pretty printing helper
def pretty_print(messages):
    # st.write("# Messages")
    for m in messages:
        if m.role == 'assistant':
            st.write(f"{m.content[0].text.value}")
    st.write()


# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.1)
    return run

def ask_model(category, indicator_statement):
    thread1, run1 = create_thread_and_run(f"""What is the {category} of the following statement: {indicator_statement}""")
    # Wait for Run 1
    run1 = wait_on_run(run1, thread1)
    st.write(f'# {category}')
    pretty_print(get_response(thread1))

if submit_button:
    
    if selected_category == 'ALL': ## if you want all the codifications, 
        for c in category_list[1:]: #run through the whole list
            ask_model(c, indicator_statement)
    else:
        ask_model(selected_category, indicator_statement)
            
    # thread1, run1 = create_thread_and_run(
    #     f"""What is the {selected_category} of the following statement: {indicator_statement}"""
    # )
    # # Wait for Run 1
    # run1 = wait_on_run(run1, thread1)
    # pretty_print(get_response(thread1))

# # Wait for Run 2
# run2 = wait_on_run(run2, thread2)
# pretty_print(get_response(thread2))

# # Wait for Run 3
# run3 = wait_on_run(run3, thread3)
# pretty_print(get_response(thread3))

# # Thank our assistant on Thread 3 :)
# run4 = submit_message(my_assistant.id, thread3, "Thank you!")
# run4 = wait_on_run(run4, thread3)
# pretty_print(get_response(thread3))
