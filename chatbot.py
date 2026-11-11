# app.py

import os
import hashlib 
from gtts import gTTS
from langdetect import detect
from io import BytesIO
import streamlit as st
from groq import Groq

# =========================
# TEXT TO SPEECH
# =========================

def speak_response(text):

    try:
        language = detect(text)

        if language == "ur":
            tts_language = "ur"
        else:
            tts_language = "en"

        audio_buffer = BytesIO()

        tts = gTTS(text=text, lang=tts_language)
        tts.write_to_fp(audio_buffer)

        audio_buffer.seek(0)

        st.audio(audio_buffer, format="audio/mp3")

    except Exception as e:
        st.warning(f"Voice error: {e}")
# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Elora AI",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded",
)

# =========================
# CUSTOM CSS & UI OVERHAUL
# =========================
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fff0f5, #f3e8ff, #fdf2f8);
    color: #59445f;
}

#MainMenu, footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}

/* Header */
.header-card {
    background: linear-gradient(135deg, #ffffff, #fce7f3);
    border: 1px solid #f3cde1;
    border-radius: 25px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 25px rgba(190, 120, 160, 0.12);
}

.header-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 65px;
    height: 65px;
    border-radius: 22px;
    font-size: 2rem;
    background: linear-gradient(135deg, #fbcfe8, #ddd6fe);
    margin-bottom: 10px;
}

.custom-title {
    font-family: 'Quicksand', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #a8558c;
    margin: 0;
}

.custom-subtitle {
    color: #9d7b9c;
    font-size: 0.9rem;
    margin-top: 8px;
}

/* Chat messages */
div[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid #f3d5e8;
    border-radius: 20px;
    padding: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 5px 15px rgba(180, 130, 170, 0.08);
}

/* User message */
div[data-testid="stChatMessage"]:has(
    div[data-testid="stChatMessageAvatarUser"]
) {
    background: #fce7f3;
    border-left: 4px solid #ec9ac5;
}

/* Assistant message */
div[data-testid="stChatMessage"]:has(
    div[data-testid="stChatMessageAvatarAssistant"]
) {
    background: #ede9fe;
    border-left: 4px solid #b6a0e8;
}

/* Chat input */
div[data-testid="stChatInput"] {
    background: white;
    border: 2px solid #f1c6df;
    border-radius: 20px;
    box-shadow: 0 5px 20px rgba(190, 120, 160, 0.12);
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #d8a5e8;
    box-shadow: 0 0 0 3px rgba(216, 165, 232, 0.2);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fce7f3, #ede9fe);
    border-right: 1px solid #eccde3;
}

section[data-testid="stSidebar"] h3 {
    color: #a8558c;
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #fbcfe8, #ddd6fe);
    color: #74466e;
    border: 1px solid #e9b8dc;
    border-radius: 14px;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #f9a8d4, #c4b5fd);
    color: #ffffff;
    border-color: #d8a5e8;
    transform: translateY(-2px);
}

/* Selectbox and slider */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label {
    color: #865d83;
    font-weight: 600;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #d8b4e2;
    border-radius: 10px;
}

::-webkit-scrollbar-track {
    background: #fff0f5;
}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown(
     """
    <div class="header-card">
        <div class="header-badge">🌸</div>
        <p class="custom-title">Elora AI</p>
        <p class="custom-subtitle">
            Your Personal AI Companion ✨
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("### 🌸 Elora AI Settings")
    model_choice = st.selectbox(
        "Model",
        ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"],
        index=0,
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    st.divider()
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
        st.rerun()
    st.caption("Built with Streamlit + Groq")

# =========================
# GROQ API KEY
# =========================
api_key = "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"

# Initialize the Groq client with your key
client = Groq(api_key=api_key)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

# =========================
# DISPLAY CHAT HISTORY
# =========================
for message in st.session_state.messages[1:]:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if "processed_audio_hash" not in st.session_state:
    st.session_state.processed_audio_hash = None
# =========================
# USER INPUT
# =========================
st.markdown("### 🎙️ Talk to Elora AI")

audio_recording = st.audio_input("Record your voice")

prompt = st.chat_input("Ask Elora AI anything...")

if audio_recording is not None:

    audio_bytes = audio_recording.getvalue()

    audio_hash = hashlib.sha256(audio_bytes).hexdigest()

    if audio_hash != st.session_state.processed_audio_hash:

        try:
            with st.spinner("🌸 Elora is listening..."):

                transcription = client.audio.transcriptions.create(
                    file=("elora_recording.wav", audio_bytes),
                    model="whisper-large-v3",
                    response_format="json",
                    temperature=0.0
                )

                prompt = transcription.text.strip()

                st.session_state.processed_audio_hash = audio_hash

                if prompt:
                    st.success("Voice converted into text!")
                    st.write("You said:", prompt)
                else:
                    st.warning("No speech detected. Please try again.")

        except Exception as e:
            st.error(f"Voice transcription error: {e}")
            prompt = None

if prompt:

    # Show user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # =========================
    # AI RESPONSE
    # =========================
    with st.chat_message("assistant", avatar="🤖"):

        message_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model=model_choice,
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=1024,
            stream=True
        )

        for chunk in stream:

            content = chunk.choices[0].delta.content

            if content:
                full_response += content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )
    # Speak AI response
    speak_response(full_response)