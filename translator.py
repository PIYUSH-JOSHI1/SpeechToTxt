import streamlit as st
from PIL import Image
from datetime import date
from gtts import gTTS
from googletrans import Translator
import speech_recognition as sr
from langdetect import detect, DetectorFactory
import os
import json
import time
import base64
from io import BytesIO

# Ensure consistent language detection
DetectorFactory.seed = 0

# App configuration
st.set_page_config(
    page_title="Indian Language Translator",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme and history
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'history' not in st.session_state:
    st.session_state.history = []

# Enhanced CSS with animations, modern styling, and theme support
st.markdown(f"""
<style>
    /* Main App Styling */
    .stApp {{
        background: {('linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)' if st.session_state.theme == 'light' else '#1E1E1E')};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: {('black' if st.session_state.theme == 'light' else 'white')};
    }}
    
    /* Header Styling */
    .main-header {{
        background: linear-gradient(90deg, #FF9933, #FFFFFF, #138808);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-in;
    }}
    
    /* Card Styling */
    .css-1r6slb0 {{
        background: {('rgba(255, 255, 255, 0.95)' if st.session_state.theme == 'light' else 'rgba(30, 30, 30, 0.95)')};
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        transition: transform 0.3s ease;
    }}
    
    .css-1r6slb0:hover {{
        transform: translateY(-5px);
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(45deg, #FF9933, #FF8033);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, #FF8033, #FF9933);
    }}
    
    /* Input Fields Styling */
    .stTextInput > div > div > input {{
        border-radius: 10px;
        border: 2px solid #FF9933;
        padding: 10px;
        transition: all 0.3s ease;
        color: {('black' if st.session_state.theme == 'light' else 'white')};
        background: {('white' if st.session_state.theme == 'light' else '#333')};
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #138808;
        box-shadow: 0 0 5px rgba(19, 136, 8, 0.3);
    }}
    
    /* Select Box Styling */
    .stSelectbox > div > div {{
        border-radius: 10px;
        border: 2px solid #FF9933;
        color: {('black' if st.session_state.theme == 'light' else 'white')};
        background: {('white' if st.session_state.theme == 'light' else '#333')};
    }}
    
    /* Progress Bar Animation */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .main-header {{
            padding: 10px;
        }}
        
        .stButton > button {{
            width: 100%;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Define Indian languages with their codes
INDIAN_LANGUAGES = {
    'hi': 'Hindi',
    'bn': 'Bengali',
    'te': 'Telugu',
    'ta': 'Tamil',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'or': 'Odia',
    'as': 'Assamese',
    'en': 'English'
}

def get_key(val, language_dict):
    """Get language code from language name"""
    for key, value in language_dict.items():
        if val == value:
            return key
    return None

def text_to_speech(text, language):
    """Convert text to speech and return audio file"""
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        st.error(f"Error in text-to-speech conversion: {str(e)}")
        return None

def main():
    # Display header with animation
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🇮🇳 Indian Language Translator")
    st.write(f"Date: {date.today()}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar for navigation and theme selection
    with st.sidebar:
        st.image("https://www.svgrepo.com/show/530444/translation.svg", width=100)
        app_mode = st.radio(
            "Choose Translation Mode",
            ["Text Translation", "Voice Translation", "Live Conversation"],
            key="navigation"
        )
        
        # Theme selection
        theme = st.selectbox(
            "Choose Theme",
            ["Light", "Dark"],
            key="theme_selection"
        )
        if theme == "Light":
            st.session_state.theme = 'light'
        else:
            st.session_state.theme = 'dark'
        
        # Display translation history
        st.subheader("Translation History")
        for item in st.session_state.history[-5:]:  # Show last 5 translations
            st.write(f"From: {item['from']}")
            st.write(f"To: {item['to']}")
            st.write(f"Original: {item['original']}")
            st.write(f"Translated: {item['translated']}")
            st.write("---")

    if app_mode == "Text Translation":
        text_translation_ui()
    elif app_mode == "Voice Translation":
        voice_translation_ui()
    elif app_mode == "Live Conversation":
        live_conversation_ui()

def text_translation_ui():
    st.header("📝 Text Translation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        input_text = st.text_area(
            "Enter text to translate",
            height=150,
            placeholder="Type or paste your text here..."
        )
        source_lang = st.selectbox(
            "Select source language",
            list(INDIAN_LANGUAGES.values()),
            key="source_lang_text"
        )
        
    with col2:
        st.markdown("### Translated Output")
        target_lang = st.selectbox(
            "Select target language",
            list(INDIAN_LANGUAGES.values()),
            key="target_lang_text"
        )
        
    if st.button("🔄 Translate", key="translate_btn"):
        if input_text:
            with st.spinner("Translating..."):
                try:
                    translator = Translator()
                    translation = translator.translate(
                        input_text,
                        src=get_key(source_lang, INDIAN_LANGUAGES),
                        dest=get_key(target_lang, INDIAN_LANGUAGES)
                    )
                    
                    st.success("Translation completed!")
                    st.markdown(f"### Translated Text:\n{translation.text}")
                    
                    # Add to history
                    st.session_state.history.append({
                        'from': source_lang,
                        'to': target_lang,
                        'original': input_text,
                        'translated': translation.text
                    })
                    
                    # Generate and play audio
                    audio_bytes = text_to_speech(
                        translation.text,
                        get_key(target_lang, INDIAN_LANGUAGES)
                    )
                    if audio_bytes:
                        st.audio(audio_bytes, format='audio/mp3')
                    
                    # Download options
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 Download Text",
                            translation.text,
                            file_name="translated_text.txt",
                            mime="text/plain"
                        )
                    with col2:
                        if audio_bytes:
                            st.download_button(
                                "🔊 Download Audio",
                                audio_bytes,
                                file_name="translation.mp3",
                                mime="audio/mp3"
                            )
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
        else:
            st.warning("Please enter some text to translate.")

def voice_translation_ui():
    st.header("🎤 Voice Translation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox(
            "Select source language",
            list(INDIAN_LANGUAGES.values()),
            key="source_lang_voice"
        )
    
    with col2:
        target_lang = st.selectbox(
            "Select target language",
            list(INDIAN_LANGUAGES.values()),
            key="target_lang_voice"
        )

    if st.button("🎙️ Start Recording", key="record_btn"):
        with st.spinner("Listening..."):
            try:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    st.info("Speak now...")
                    audio = r.listen(source, timeout=5)
                    text = r.recognize_google(
                        audio,
                        language=get_key(source_lang, INDIAN_LANGUAGES)
                    )
                    
                    st.write(f"Recognized Text: {text}")
                    
                    translator = Translator()
                    translation = translator.translate(
                        text,
                        src=get_key(source_lang, INDIAN_LANGUAGES),
                        dest=get_key(target_lang, INDIAN_LANGUAGES)
                    )
                    
                    st.success(f"Translated Text: {translation.text}")
                    
                    # Add to history
                    st.session_state.history.append({
                        'from': source_lang,
                        'to': target_lang,
                        'original': text,
                        'translated': translation.text
                    })
                    
                    audio_bytes = text_to_speech(
                        translation.text,
                        get_key(target_lang, INDIAN_LANGUAGES)
                    )
                    if audio_bytes:
                        st.audio(audio_bytes, format='audio/mp3')
                        
                    # Download options
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 Download Text",
                            translation.text,
                            file_name="voice_translation.txt",
                            mime="text/plain"
                        )
                    with col2:
                        if audio_bytes:
                            st.download_button(
                                "🔊 Download Audio",
                                audio_bytes,
                                file_name="voice_translation.mp3",
                                mime="audio/mp3"
                            )
            except sr.UnknownValueError:
                st.error("Sorry, I couldn't understand the audio.")
            except sr.RequestError:
                st.error("Sorry, there was an issue with the speech recognition service.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def live_conversation_ui():
    st.header("💬 Live Conversation")
    st.write("Real-time translation between two speakers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        lang1 = st.selectbox(
            "Speaker 1 Language",
            list(INDIAN_LANGUAGES.values()),
            key="lang1"
        )
        
    with col2:
        lang2 = st.selectbox(
            "Speaker 2 Language",
            list(INDIAN_LANGUAGES.values()),
            key="lang2"
        )

    conversation_active = st.checkbox("Start Conversation")
    
    if conversation_active:
        try:
            while conversation_active:
                # Speaker 1's turn
                with st.container():
                    st.write("👤 Speaker 1's turn...")
                    if st.button("🎤 Record Speaker 1"):
                        record_and_translate(
                            lang1, lang2,
                            "Speaker 1", "Speaker 2"
                        )
                
                # Speaker 2's turn
                with st.container():
                    st.write("👤 Speaker 2's turn...")
                    if st.button("🎤 Record Speaker 2"):
                        record_and_translate(
                            lang2, lang1,
                            "Speaker 2", "Speaker 1"
                        )
                
                time.sleep(0.1)  # Prevent excessive CPU usage
                
        except Exception as e:
            st.error(f"An error occurred in the conversation: {str(e)}")

def record_and_translate(src_lang, dest_lang, speaker_from, speaker_to):
    """Record audio and translate it"""
    try:
        with st.spinner(f"Recording {speaker_from}'s voice..."):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(
                    audio,
                    language=get_key(src_lang, INDIAN_LANGUAGES)
                )
                
                st.write(f"{speaker_from} said: {text}")
                
                translator = Translator()
                translation = translator.translate(
                    text,
                    src=get_key(src_lang, INDIAN_LANGUAGES),
                    dest=get_key(dest_lang, INDIAN_LANGUAGES)
                )
                
                st.success(f"To {speaker_to}: {translation.text}")
                
                # Add to history
                st.session_state.history.append({
                    'from': src_lang,
                    'to': dest_lang,
                    'original': text,
                    'translated': translation.text
                })
                
                audio_bytes = text_to_speech(
                    translation.text,
                    get_key(dest_lang, INDIAN_LANGUAGES)
                )
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3')
                    
    except Exception as e:
        st.error(f"Error in recording/translation: {str(e)}")

if __name__ == "__main__":
    main()
