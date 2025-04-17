import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()  # Ensure you have a .env file with GOOGLE_API_KEY
import google.generativeai as genai
print(genai.__version__)
import streamlit as st
from PIL import Image  # Import PIL to handle image processing



# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to load Gemini Pro Vision model
def load_gemini_pro_vision_model():
    """
    Load the Gemini Pro Vision model.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model name
    return model

# Initialize the Streamlit app
st.set_page_config(page_title="Image Verification Demo", page_icon="🔮", layout="wide")
st.header("Gemini Image Verification Application")

# Input fields
input_txt = st.text_area("Ask a question:", key="input")
input_img = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"], key="image")

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