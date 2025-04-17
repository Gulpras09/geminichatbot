import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()  # Make sure .env contains GOOGLE_API_KEY

# Streamlit UI for API Key input (optional if not using .env)
st.set_page_config(page_title="Image Verification Demo",
                   page_icon="🔮", layout="wide")
st.header("Gemini Image Verification Application")

# Get API key securely from .env or manual input
api_key = os.getenv("GOOGLE_API_KEY") or st.text_input(
    "Enter your Google API Key", type="password")

# Validate API key
if not api_key:
    st.error(
        "❌ Google API key is missing! Please set it in your .env or enter it above.")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"❌ Failed to configure Gemini API: {e}")
    st.stop()

# Function to load Gemini Pro Vision model


def load_gemini_pro_vision_model():
    """
    Load the Gemini Pro Vision model.
    """
    model = genai.GenerativeModel(
        "gemini-1.5-flash")  # or your preferred version
    return model


# Input fields
input_txt = st.text_area("Ask a question:", key="input")
input_img = st.file_uploader("Upload an image:", type=[
                             "jpg", "jpeg", "png"], key="image")

# Display uploaded image
if input_img is not None:
    image = Image.open(input_img)
    st.image(image, caption='Uploaded Image', use_container_width=True)

# If ask button is clicked
if st.button("Ask"):
    try:
        # Validate inputs
        if not input_txt.strip():
            st.warning("Please enter a question.")
        elif input_img is None:
            st.warning("Please upload an image.")
        else:
            # Load the model
            model = load_gemini_pro_vision_model()

            # Convert the uploaded file to a PIL Image
            pil_image = Image.open(input_img)

            # Generate response
            response = model.generate_content([input_txt, pil_image])

            # Display response
            st.subheader("Response:")
            st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred: {e}")
