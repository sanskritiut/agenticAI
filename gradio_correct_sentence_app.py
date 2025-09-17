import gradio as gr
import assemblyai as aai
from openai import OpenAI
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import uuid
from pathlib import Path
import os

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSEMBLYAI_KEY = os.getenv("ASSEMBLYAI_KEY")
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


def process_audio(audio_file):
    transcription_response = audio_transcription(audio_file)

    if transcription_response.status == aai.TranscriptStatus.error:
        raise gr.Error(transcription_response.error)
    else:
        text = transcription_response.text
       
    
    correct_sentence = generate_ai_response_Gemini(text)
    print("correct_sentence")
    print(correct_sentence)
    correct_sentence_audio_path = text_to_speech(correct_sentence)
    correct_sentence_path = Path(correct_sentence_audio_path)

    # Your audio processing function here
    
    return correct_sentence_path

def text_to_speech(text):
    print("text_to_speech")
    print(text)
    elevenlabs = ElevenLabs(
        api_key=ELEVENLABS_API_KEY,
    )
    response = elevenlabs.text_to_speech.convert(
        voice_id="3sWiBfwPqw7lQWQkCbej", 
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5", # use the turbo model for low latency
        # Optional voice settings that allow you to customize the output
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=1.0,
            style=0.5,
            use_speaker_boost=True,
            speed=0.9,
        ),
    )
    # uncomment the line below to play the audio back
    # play(response)
    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"
    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
    
    # Return the path of the saved audio file
    return save_file_path

def generate_ai_response(transcript):
    openai_client = OpenAI(api_key = OPENAI_API_KEY)
    full_transcript = [
        {"role":"system", "content":"You are an expert English language tutor and grammar correction agent. Your sole purpose is to receive a spoken utterance from the user, analyze it for grammatical errors, unnatural phrasing, and poor sentence structure, and return only the **single, corrected version of the user's sentence**. Do not offer explanations, commentary,  Only output the corrected sentence. If the user's input is perfectly correct, repeat the input sentence back exactly."}
    ]
    full_transcript.append({"role":"user", "content": transcript})
        

    response = openai_client.chat.completions.create(
        model = "gpt-4.1",
        messages = full_transcript
    )

    ai_response = response.choices[0].message.content
    return ai_response

def generate_ai_response_Gemini(transcript):
    
    full_transcript = [
        {"role":"system", "content":"You are an expert English language tutor and grammar correction agent. Your sole purpose is to receive a spoken utterance from the user, analyze it for grammatical errors, unnatural phrasing, and poor sentence structure, and return only the **single, corrected version of the user's sentence**. Do not offer explanations, commentary,  Only output the corrected sentence. If the user's input is perfectly correct, repeat the input sentence back exactly."}
    ]
    full_transcript.append({"role":"user", "content": transcript})
        
    gemini = OpenAI(api_key=GOOGLE_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    model_name = "gemini-2.0-flash"

    response = gemini.chat.completions.create(model=model_name, messages=full_transcript)
    ai_response = response.choices[0].message.content
    return ai_response
    

        
def audio_transcription(audio_file):
    aai.settings.api_key = ASSEMBLYAI_KEY
    transcriber = aai.Transcriber()
    transcription = transcriber.transcribe(audio_file)
    return transcription

audio_input = gr.Audio(
    sources=["microphone"],
    type="filepath"
)

demo = gr.Interface(
    fn=process_audio,
    inputs=audio_input,
    outputs=[gr.Audio(label="English")]
)

demo.launch()
