'''

this code creates a user-friendly interface that allows users to upload a text file, provide input messages,and receive responses generated by a language model 
It leverages Azure Blob Storage for file storage and retrieval, providing a simple way to interact with a language model for conversational tasks,
and generating responses based on user input and uploaded data.
'''


import streamlit as st
import openai
import os
from dotenv import load_dotenv
from helper import upload_file_to_blob, read_blob_data

# Configure OpenAI API
load_dotenv('.env')
openai.api_type = os.getenv('api_type')
openai.api_base = os.getenv('api_base')
openai.api_version = os.getenv('api_version')
openai.api_key = os.getenv('api_key')

# Azure Blob Storage configuration
STORAGEACCOUNTURL = os.getenv('STORAGEACCOUNTURL')
STORAGEACCOUNTKEY = os.getenv('STORAGEACCOUNTKEY')
CONTAINERNAME = os.getenv('CONTAINERNAME')

st.set_page_config(page_title="Ask your Data")
st.header("Ask your data 💬")

# Upload file
file = st.file_uploader("Upload your file", type=["txt"])
if file:
    file_name = upload_file_to_blob(file, STORAGEACCOUNTURL, STORAGEACCOUNTKEY, CONTAINERNAME)
    st.success(f"File '{file_name}' uploaded to '{CONTAINERNAME}/{file_name}'")

    # Retrieve 
    data = read_blob_data(STORAGEACCOUNTURL, STORAGEACCOUNTKEY, CONTAINERNAME, file_name)
    # st.text("Uploaded Text Data:")
    # st.text(data)

    user_input = st.text_input("You:", "")
    if st.button("Generate"):
        # Include the uploaded data and user input
        input_prompt = f"Uploaded Data:\n{data}\nUser Input: {user_input}"

        response = openai.Completion.create(
            engine="restaurant",
            prompt=input_prompt,
            temperature=1,
            max_tokens=100,
            top_p=0.5,
            frequency_penalty=0,
            presence_penalty=0,
            best_of=1,
            stop=None
        )

        assistant_reply = response.choices[0].text.strip()
        st.text("Assistant:")
        st.text(assistant_reply)


