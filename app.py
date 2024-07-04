import streamlit as st
import azure.cognitiveservices.speech as speechsdk

# Azure Speech configuration
speech_key = st.secrets["azure_key"]
service_region = st.secrets["azure_service_region"]

def get_speech_config(language):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    if language == "English":
        speech_config.speech_recognition_language = "en-IN"
    elif language == "Hindi":
        speech_config.speech_recognition_language = "hi-IN"
    return speech_config

def recognize_speech(language):
    speech_config = get_speech_config(language)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return f"No speech could be recognized in {language}"
    elif result.reason == speechsdk.ResultReason.Canceled:
        return f"Speech recognition canceled for {language}"

st.title("Bilingual Real-time Speech-to-Text")

if 'text_output' not in st.session_state:
    st.session_state.text_output = []

language = st.selectbox("Select Language", ["English", "Hindi"])

start_button = st.button("Start Listening")

if start_button:
    st.write(f"Listening in {language}... Speak now.")
    result = recognize_speech(language)
    st.session_state.text_output.append(f"[{language}] {result}")
    st.write(f"Speech recognized in {language}. Click 'Start Listening' again to continue.")

st.subheader("Recognized Text:")
for text in st.session_state.text_output:
    st.write(text)

clear_button = st.button("Clear Output")
if clear_button:
    st.session_state.text_output = []
    st.experimental_rerun()
