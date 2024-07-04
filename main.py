import azure.cognitiveservices.speech as speechsdk
import time

def azure_speech_to_text():
    # Replace with your own subscription key and region
    speech_key = "ae7465dd86834f55bc4f377ea902b18c"
    service_region = "centralindia"

    # Create speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language = "en-US"

    # Create audio configuration for the default microphone
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create speech recognizer
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")

    def recognized_cb(evt):
        print(f"RECOGNIZED: {evt.result.text}")

    def canceled_cb(evt):
        print(f"CANCELED: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {evt.error_details}")

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.canceled.connect(canceled_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        speech_recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    azure_speech_to_text()