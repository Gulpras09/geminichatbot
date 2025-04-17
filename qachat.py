from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()  # Ensure you have a .env file with GOOGLE_API_KEY

# Configure Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    st.error("Missing API key! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Function to load Gemini Pro model and get response
def get_gemini_response(question):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-001")
        chat = model.start_chat(history=[])
        response = chat.send_message(question, stream=True)

        full_response = ""
        for chunk in response:
            if hasattr(chunk, "text") and chunk.text:  # Ensure valid text response
                full_response += chunk.text
            else:
                st.warning("Received an empty response from the AI.")
                return "No valid response received."

        return full_response

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "Error processing the request."

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo", page_icon="🔮", layout="wide")
st.header("Gemini LLM Application")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

input_text = st.text_input("Enter your question:", key="input")
submit = st.button("Ask the Question")

if submit and input_text.strip():  # Avoid empty inputs
    response = get_gemini_response(input_text)

    # Ensure only valid tuples are added to chat history
    if isinstance(input_text, str) and isinstance(response, str):
        st.session_state["chat_history"].append(("You", input_text))
        st.session_state["chat_history"].append(("Bot", response))
    else:
        st.error("Invalid response format detected.")

# Display chat history
st.subheader("Chat History:")
for entry in st.session_state["chat_history"]:
    if isinstance(entry, tuple) and len(entry) == 2:
        role, text = entry  # Unpack the tuple correctly
        st.write(f"**{role}:** {text}")
    else:
        st.error("Unexpected data format in chat history.")
