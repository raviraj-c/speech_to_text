import azure.cognitiveservices.speech as speechsdk
import streamlit as st
# Your subscription key and service region
# speech_key, service_region = "ae7465dd86834f55bc4f377ea902b18c", "centralindia"
speech_key = st.secrets["azure_key"]
service_region = st.secrets["azure_service_region"]

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Use the default microphone as the audio input
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
print("Say something...")

result = speech_recognizer.recognize_once()

# Check the result
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: NoMatch")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))

# Additional debug information
if result is not None:
    print("Duration: {}".format(result.duration))
    print("Offset: {}".format(result.offset))
else:
    print("No result returned")

