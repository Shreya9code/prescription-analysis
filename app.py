import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
#from googletrans import Translator

# Configure Gemini AI API
genai.configure(api_key="AIzaSyAJiWbzaJJFQGwZAANH4uDKKIAsedDDqVI")  # Replace with your actual API Key

model = genai.GenerativeModel('gemini-1.5-flash')

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image[0], prompt])
    return response.text

# Page configuration for a clean, organized interface
st.set_page_config(page_title="Prescription Reader", page_icon="🩺", layout="wide")

# Styling with Markdown and Custom CSS
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .subheading {
        font-size: 26px;
        color: #3b3b3b;
        font-weight: 600;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .section-heading {
        font-size: 24px;
        color: #333;
        font-weight: bold;
        padding: 10px;
        background-color: #e1f7d5;
        border-radius: 8px;
        margin-top: 20px;
        text-align: center;
    }
    .instructions {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
    }
    .button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        font-size: 18px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .button:hover {
        background-color: #45a049;
    }
    .file-uploader {
        text-align: center;
    }
    .output-container {
        background-color: #f4f4f9;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
    }
    .output-container h2 {
        color: #4CAF50;
        font-size: 22px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">🩺 AI-Powered Prescription Reader</h1>', unsafe_allow_html=True)

# Introduction Section
st.markdown("""
    <div class="instructions">
        <h2 class="subheading">🏥 Welcome to **CureConnect**!</h2>
        <p>Use our AI-powered tool to analyze and understand your medical prescriptions.</p>
    </div>
""", unsafe_allow_html=True)

# Input for question and file upload
question = st.text_input("Ask about your prescription:", key="input", label_visibility="collapsed")
uploaded_file = st.file_uploader("Upload your prescription (JPG, PNG, JPEG)", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Prescription", use_column_width=True, output_format="PNG")

# Translation Settings Section
#st.subheader("🌍 Translation Settings")
#st.markdown("""
#    Choose the target language for translation (optional).  
 #   **Note:** If you select **None**, the results will be shown in English.
#""")
#target_language = st.selectbox("Select target language:", ["None", "en", "es", "fr", "de", "zh-cn", "hi", "ja", "ko", "pt", "ru", "bn", "bh", "gu", "ks", "ml", "ko", "mr", "ne", "or", "pa", "sa", "ta", "te"])

# Analyze Prescription Button
submit = st.button("🔍 Analyze Prescription", key="submit_button", help="Click to analyze the prescription")

# Output Section (Results)
if submit:
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        input_prompt = "You are an expert in medical prescriptions. Analyze the image and answer queries."
        medicine_prompt1 = "Extract medicine details (name, uses, side effects, safety tips)."
        medicine_prompt2 = " Also predict for what steps users can take to cure her disease besides medicines"

        # Get responses from Gemini model
        response = get_gemini_response(input_prompt, image_data, question)
        medicine_details1 = get_gemini_response(medicine_prompt1, image_data, "")
        medicine_details2 = get_gemini_response(medicine_prompt2, image_data, "")

        # Display Results
        st.markdown("<div class='output-container'><h2 class='subheading'>📝 Prescription Analysis:</h2></div>", unsafe_allow_html=True)
        st.write(response)
        st.markdown("<div class='output-container'><h2 class='subheading'>💊 Extracted Medicine Details:</h2></div>", unsafe_allow_html=True)
        st.write(medicine_details1)
 # Additional Steps Heading with Custom Styling
        st.markdown("<div class='section-heading'>🌱 Additional Steps to Cure the Disease (Beyond Medication)</div>", unsafe_allow_html=True)
        st.write("Here, the system will provide suggestions for steps beyond just taking medicine. These could include lifestyle changes, exercise, diet improvements, mental health tips, and more.")

        st.write(medicine_details2)

       
        # Handle translation
        #if target_language != "None":
        #    translator = Translator()
         #   translation = translator.translate(medicine_details1, dest=target_language)
          #  st.subheader(f"Translated to {target_language.upper()}:")
           # st.write(translation.text)
    #else:
     #   st.error("⚠️ Please upload a prescription image.")

# Instructions Section
st.subheader("📌 How to Use:")
st.markdown("""
1. **📤 Upload Your Prescription:**  
   Click on the **"Browse files"** button and select an image of your handwritten medical prescription  
   (Supported formats: **JPG, JPEG, PNG**).
   
2. **🤖 Click 'Analyze Prescription':**  
   Press the **"Analyze Prescription"** button to extract and analyze the medicines mentioned.

3. **📋 Review Results:**  
   The AI will generate a **detailed breakdown** of the prescription, including:
   - Medicine names  
   - Their dosage  
   - Side effects  
   - Safety advice
""")
