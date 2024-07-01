import io
import os
from google.cloud import speech
import pyaudio

# Set your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google-credentials.json"



def google_speech_to_text():
    # Audio recording parameters
    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    def generate_requests():
        audio_input = pyaudio.PyAudio()
        stream = audio_input.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        while True:
            data = stream.read(CHUNK)
            yield speech.StreamingRecognizeRequest(audio_content=data)

    def listen_print_loop(responses):
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            if result.is_final:
                print(f"Final: {transcript}")
            else:
                print(f"Interim: {transcript}")

    print("Listening, say something!")

    stream = client.streaming_recognize(streaming_config, generate_requests())

    try:
        listen_print_loop(stream)
    except KeyboardInterrupt:
        print("Stopping...")

if __name__ == "__main__":
    google_speech_to_text()