import assemblyai as aai
from assemblyai.streaming.v3 import (
    BeginEvent,
    StreamingClient,
    StreamingClientOptions,
    StreamingError,
    StreamingEvents,
    StreamingParameters,
    StreamingSessionParameters,
    TerminationEvent,
    TurnEvent,
)
import logging
from typing import Type
from typing import Type
from elevenlabs import generate, stream
from openai import OpenAI
from dotenv import load_dotenv
import uuid
from pathlib import Path
import os

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSEMBLYAI_KEY = os.getenv("ASSEMBLYAI_KEY")


# Replace with your chosen API key, this is the "default" account api key
api_key = ASSEMBLYAI_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
aai.settings.api_key = ASSEMBLYAI_KEY
openai_client = OpenAI(api_key = OPENAI_API_KEY)
elevenlabs_api_key = ELEVENLABS_API_KEY

transcriber = None

        # Prompt
full_transcript = [
    {"role":"system", "content":"You are an expert English language tutor and grammar correction agent. Your sole purpose is to receive a spoken utterance from the user, analyze it for grammatical errors, unnatural phrasing, and poor sentence structure, and return only the **single, corrected version of the user's sentence**. Do not offer explanations, commentary,  Only output the corrected sentence. If the user's input is perfectly correct, repeat the input sentence back exactly."}
]

def on_begin(self,event: BeginEvent):
    print(f"Session started: {event.id}")

def on_turn(self, event: TurnEvent):
    print(f"turn {event.transcript} ({event.end_of_turn})")

    
    if event.end_of_turn :
        print("I am vineet")
        generate_ai_response(event.transcript)
        
        
def on_terminated(self,event: TerminationEvent):
    print(
        f"Session terminated: {event.audio_duration_seconds} seconds of audio processed"
    )

def on_error(self, error: StreamingError):
    print(f"Error occurred: {error}")

def stop_transcription():
    
    transcriber = None

def start_transcription():
    client = StreamingClient(
        StreamingClientOptions(
            api_key=api_key,
            api_host="streaming.assemblyai.com",
        )
    )

    client.on(StreamingEvents.Begin, on_begin)
    client.on(StreamingEvents.Turn, on_turn)
    client.on(StreamingEvents.Termination, on_terminated)
    client.on(StreamingEvents.Error, on_error)

    client.connect(
        StreamingParameters(
            sample_rate = 16000
            
        )
    )

    try:
        client.stream(
            aai.extras.MicrophoneStream(sample_rate=16000)
        )
    finally:
        client.disconnect(terminate=True)

def generate_ai_response(transcript):

        stop_transcription()

        full_transcript.append({"role":"user", "content": transcript})
        print(f"\nPatient: {transcript}", end="\r\n")

        response = openai_client.chat.completions.create(
            model = "gpt-4.1",
            messages = full_transcript
        )

        ai_response = response.choices[0].message.content

        generate_audio(ai_response)

        start_transcription()
        print(f"\nReal-time transcription: ", end="\r\n")


def generate_audio(text):

    full_transcript.append({"role":"assistant", "content": text})
    print(f"\nAI Receptionist: {text}")

    audio_stream = generate(
        api_key = elevenlabs_api_key,
        text = text,
        voice = "3sWiBfwPqw7lQWQkCbej",
        stream = True
    )

    stream(audio_stream)


if __name__ == "__main__":
    greeting = "Thank you for calling, how may I assist you?"
    generate_audio(greeting)
    start_transcription()