from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Google Generative AI with the API key
genai.configure(api_key=api_key)

# Load Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("WELCOME TO QUIZ BUDDY CHATBOT")

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

st.markdown(
    "<h1 style='font-size:30px;'>HOW MAY I HELP YOU?</h1>",
    unsafe_allow_html=True
)

# The actual input field
input = st.text_input("", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
