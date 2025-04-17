from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Streamlit app configuration
st.set_page_config(page_title="Q&A Demo", page_icon="🔮", layout="wide")
st.header("Gemini LLM Application")

# Try to get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")

# If not found in .env, ask the user to input it
if not api_key:
    api_key = st.text_input(
        "Enter your Google Generative AI API Key:", type="password")
    if not api_key:
        st.info("Please enter your API key to continue.", icon="🗝️")
        st.stop()

# Try configuring Gemini with the provided API key
try:
    genai.configure(api_key=api_key)

    # Validate API key with a test prompt
    test_model = genai.GenerativeModel("gemini-1.5-flash-001")
    _ = test_model.generate_content("Hello!").text

except Exception as e:
    st.error("Invalid or unauthorized API key. Please double-check and try again.")
    st.stop()

# Function to get response from Gemini model


def get_gemini_response(question):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-001")
        chat = model.start_chat(history=[])
        response = chat.send_message(question, stream=True)

        full_response = ""
        for chunk in response:
            if hasattr(chunk, "text") and chunk.text:
                full_response += chunk.text
            else:
                st.warning("Received an empty response from the AI.")
                return "No valid response received."

        return full_response

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "Error processing the request."


# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input for question
input_text = st.text_input("Enter your question:", key="input")
submit = st.button("Ask the Question")

if submit and input_text.strip():
    response = get_gemini_response(input_text)

    if isinstance(input_text, str) and isinstance(response, str):
        st.session_state["chat_history"].append(("You", input_text))
        st.session_state["chat_history"].append(("Bot", response))
    else:
        st.error("Invalid response format detected.")

# Display chat history
st.subheader("Chat History:")
for entry in st.session_state["chat_history"]:
    if isinstance(entry, tuple) and len(entry) == 2:
        role, text = entry
        st.write(f"**{role}:** {text}")
    else:
        st.error("Unexpected data format in chat history.")
