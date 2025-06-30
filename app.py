import streamlit as st
from streamlit_lottie import st_lottie
from gemini_utils import get_gift_ideas_from_text, get_gift_ideas_from_image
from PIL import Image
import requests
import os

# Page config
st.set_page_config(page_title="GiftGenie.AI 🎁", page_icon="🎁", layout="centered")

# Lottie animation loader
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_gift = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jbrw3hcz.json")

# CSS Styling
st.markdown("""
    <style>
        .stTextInput > div > div > input {
            font-size: 18px;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        .stButton > button {
            background-color: #7b2cbf;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-size: 16px;
        }
        .gift-card {
            background-color: #fff0f5;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            color: #333;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# App layout
st_lottie(lottie_gift, height=200, key="gift")
st.title("🎁 GiftGenie.AI")
st.subheader("Get personalized gift suggestions based on mood, text, or image!")

option = st.radio("Choose input mode:", ["Text Only", "Text + Image"])

user_text = st.text_input("Describe the person or occasion:")

if option == "Text + Image":
    uploaded_file = st.file_uploader("Upload an image (optional):", type=["jpg", "png", "jpeg"])
    if st.button("✨ Get Gift Ideas"):
        if not user_text and not uploaded_file:
            st.warning("Please enter a description or upload an image.")
        else:
            with st.spinner("Generating gift suggestions..."):
                if uploaded_file:
                    with open("temp_img.png", "wb") as f:
                        f.write(uploaded_file.getvalue())
                    result = get_gift_ideas_from_image("temp_img.png", user_text)
                    os.remove("temp_img.png")
                else:
                    result = get_gift_ideas_from_text(user_text)
                st.success("Here are some suggestions!")
                for line in result.strip().split("\n"):
                    if line.strip():
                        st.markdown(f"<div class='gift-card'>{line.strip()}</div>", unsafe_allow_html=True)
else:
    if st.button("✨ Get Gift Ideas"):
        if not user_text:
            st.warning("Please enter some description.")
        else:
            with st.spinner("Generating gift suggestions..."):
                result = get_gift_ideas_from_text(user_text)
                st.success("Here are some suggestions!")
                for line in result.strip().split("\n"):
                    if line.strip():
                        st.markdown(f"<div class='gift-card'>{line.strip()}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<center>Made with ❤️ using Google Gemini + Streamlit</center>", unsafe_allow_html=True)