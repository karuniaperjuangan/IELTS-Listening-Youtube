import streamlit as st
import dotenv
import os
from yt_dlp import YoutubeDL
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import json

# Load environment variables
dotenv.load_dotenv()

# Streamlit app layout
st.title("IELTS Listening Task Generator from YouTube")

# Input for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL", value="")
audio_file_path = "./audio.mp3"

# Function to download and transcribe audio
def transcribe_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './audio.%(ext)s',
        'ffmpeg_location': os.getenv('FFMPEG_PATH'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    client = OpenAI()
    audio_file = open("./audio.mp3", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    
    return transcription.text

# Video preview
if youtube_url:
    video_id = youtube_url.split("v=")[-1]
    st.video(f"https://www.youtube.com/embed/{video_id}")
    with st.spinner("Downloading and transcribing audio..."):
        # Allow user to play the audio file
        st.subheader("Audio Playback")
        with open(audio_file_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3") 

# Define model for IELTS listening task
class IELTSListeningTask(BaseModel):
    question_text: str
    answers: List[str]

# Function to generate IELTS listening questions
def generate_ielts_questions(transcription_text):
    client = OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a teacher preparing an IELTS listening test. You have a transcription of an audio file."\
                    "You want to generate a set of listening questions based on the audio file. The questions should be fill in the blanks of"\
                    " one-two paragraphs as in IELTS format with about 10-15 questions. The text must not be verbatim from the audio file and the text structure can be reparaphrased or very different from the original instruction, but keep in mind that the answers must can be inferred from the transcription and in order as in the transcription. Don't forget to number the blanks in the questions. Example: The capital of France is ____(1) which is known as the city of ____(2)."
            },
            {"role": "user", "content": "Transcription: " + transcription_text},
        ],
        response_format=IELTSListeningTask
    )
    
    return json.loads(response.choices[0].message.content)

# Check if transcription and task are in session state
if 'transcription_text' not in st.session_state:
    st.session_state['transcription_text'] = ''
if 'task' not in st.session_state:
    st.session_state['task'] = None
if 'audio' not in st.session_state:
    st.session_state['audio'] = None

# Button to process the input and generate questions
if st.button("Generate IELTS Listening Task"):  
    with st.spinner("Generating IELTS listening questions..."):
        st.session_state['transcription_text'] = transcribe_audio(youtube_url)
        st.session_state['task'] = generate_ielts_questions(st.session_state['transcription_text'])
        st.subheader("Generated IELTS Listening Questions")
        st.write(st.session_state['task']["question_text"])

# Display the transcription and task if they are available
if st.session_state['task']:
    st.subheader("Generated IELTS Listening Questions")
    st.write(st.session_state['task']["question_text"])

    # Option to show transcription
    if st.checkbox("Show Transcription"):
        st.write(st.session_state['transcription_text'])

    # Option to show answers
    if st.checkbox("Show Answers"):
        st.subheader("Answers")
        for i, answer in enumerate(st.session_state['task']["answers"], 1):
            st.write(f"{i}. {answer}")
