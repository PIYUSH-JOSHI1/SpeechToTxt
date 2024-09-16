import streamlit as st  # building web apps in python
from PIL import Image  # for opening image files
from datetime import date  # provides date & time functions
from gtts import gTTS, lang  # for text speech
from googletrans import Translator  # provides translation functions
import speech_recognition as sr  # for speech recognition
from langdetect import detect, DetectorFactory  # for language detection

# Ensure consistent language detection
DetectorFactory.seed = 0

# setting app's title, icon & layout
st.set_page_config(page_title="Simply! Translate", page_icon="🎯")

def get_key(val):
    """Function to find the key of the given value in the dict object

    Args:
        val (str): value to find key

    Returns:
        key(str): key for the given value
    """
    for key, value in lang.tts_langs().items():
        if val == value:
            return key

def main():
    # instance of Translator()
    trans = Translator()

    # gets gtts supported languages as dict
    langs = lang.tts_langs()
    language_options = list(langs.values())
    lang_keys = list(langs.keys())

    # display current date & header
    st.header("Translate your thoughts.")
    st.write(f"Date : {date.today()}")

    input_text = st.text_input("Enter text to translate")  # gets text to translate
    lang_choice = st.selectbox(
        "Language to translate to: ", language_options
    )  # shows the supported languages list as selectbox options

    if st.button("Translate Text"):
        if input_text == "":
            # if the user input is empty
            st.write("Please Enter text to translate")

        else:
            detect_lang = detect(input_text)  # detect the language of the input text
            detect_text = f"Detected Language : {langs.get(detect_lang, 'Unknown')}"
            st.success(detect_text)  # displays the detected language

            # convert the detected text to audio file
            detect_audio = gTTS(text=input_text, lang=detect_lang, slow=False)
            detect_audio.save("user_detect.mp3")
            audio_file = open("user_detect.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/ogg", start_time=0)

            # Translate the input text
            translation = trans.translate(input_text, dest=get_key(lang_choice))
            translation_text = f"Translated Text: {translation.text}"
            st.success(translation_text)  # displays the translated text

            # convert the translated text to audio file
            translated_audio = gTTS(text=translation.text, lang=get_key(lang_choice), slow=False)
            translated_audio.save("user_trans.mp3")
            audio_file = open("user_trans.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/ogg", start_time=0)

            # download button to download translated audio file
            with open("user_trans.mp3", "rb") as file:
                st.download_button(
                    label="Download Translated Audio",
                    data=file,
                    file_name="trans.mp3",
                    mime="audio/ogg",
                )

    # Speech to Text feature
    st.header("Speech to Text")
    speech_recognizer = sr.Recognizer()

    with st.expander("Record Audio"):
        st.write("Click the record button to start speaking")
        record_button = st.button("Record")
        if record_button:
            with sr.Microphone() as source:
                st.write("Recording...")
                audio = speech_recognizer.record(source, duration=5)
                try:
                    text = speech_recognizer.recognize_google(audio, language="en-US")
                    st.write(f"Recognized Text: {text}")

                    # Auto-detect language
                    detected_lang = detect(text)
                    detected_lang_name = langs.get(detected_lang, 'Unknown')
                    st.write(f"Detected Language: {detected_lang_name}")

                    # Save recognized text to a .txt file
                    with open("recognized_text.txt", "w") as file:
                        file.write(text)

                    # Provide download button for the text file
                    with open("recognized_text.txt", "r") as file:
                        st.download_button(
                            label="Download Recognized Text",
                            data=file,
                            file_name="recognized_text.txt",
                            mime="text/plain",
                        )

                    # Translate recognized text
                    st.subheader("Translate Recognized Text")
                    target_lang_choice = st.selectbox(
                        "Select Language to Translate Recognized Text to:",
                        language_options
                    )
                    if st.button("Translate Recognized Text"):
                        translation = trans.translate(text, dest=get_key(target_lang_choice))
                        translated_text = f"Translated Text: {translation.text}"
                        st.write(translated_text)

                        # Save the translated text to a file
                        with open("translated_text.txt", "w") as file:
                            file.write(translation.text)

                        # Provide download button for the translated text file
                        with open("translated_text.txt", "r") as file:
                            st.download_button(
                                label="Download Translated Text",
                                data=file,
                                file_name="translated_text.txt",
                                mime="text/plain",
                            )

                except sr.UnknownValueError:
                    st.write("Sorry, I didn't catch that. Please try again.")
                except sr.RequestError:
                    st.write("Sorry, there was an issue with the speech recognition service.")

if __name__ == "__main__":
    main()  # calls the main() first
