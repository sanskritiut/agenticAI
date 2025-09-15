This setup document provides instructions for installing and configuring your English Language Tutor application, which uses Gradio for the user interface, AssemblyAI for speech-to-text, OpenAI for grammar correction, and ElevenLabs for text-to-speech.

English Language Tutor: Setup Document
This guide outlines the steps required to set up and run the Gradio application code.

# Prerequisites
Before you begin, ensure you have the following accounts and information:

Python: Version 3.8 or higher installed.

API Keys:

OpenAI API Key (for grammar correction)

AssemblyAI API Key (for audio transcription)

ElevenLabs API Key (for text-to-speech)

# Environment Setup
Create and Activate Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.

Bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Activate the virtual environment (Windows)
.\venv\Scripts\activate

# Install Required Libraries
Install all necessary Python packages using pip.
pip install gradio assemblyai openai elevenlabs python-dotenv

# Configuration and API Keys
This application uses environment variables to securely load your API keys.

Create the .env File
Create a file named .env in the root directory of your project (where your Python script is saved).

Add API Keys to .env
Add your API keys to the .env file using the following format. Replace the placeholder text with your actual keys.

# .env file content
ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY_HERE"

OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"

ASSEMBLYAI_KEY="YOUR_ASSEMBLYAI_KEY_HERE"

# Run the Application
Once the environment is set up, dependencies are installed, and the .env file is configured, you can run the application.


# Assuming your code is saved as gradio_correct_sentence_app.py 
python gradio_correct_sentence_app.py 

Expected Output
The command will start the Gradio server and provide a local URL (e.g., http://127.0.0.1:7860/) and a Public URL (e.g., https://xxxxxx.gradio.app).

Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://xxxxxx.gradio.app
...
Open the provided URL in your web browser to interact with the English Language Tutor application. You can now use your microphone to record a sentence, and the application will return the corrected audio.
