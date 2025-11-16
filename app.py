import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
import wave
import tempfile

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Personality configurations
PERSONALITIES = {
    "General Assistant": {
        "name": "General Assistant",
        "icon": "🤖",
        "system_prompt": "You are a helpful and friendly AI assistant. Provide clear, accurate, and helpful responses to user questions.",
        "description": "A versatile AI assistant ready to help with various topics."
    },
    "Study Buddy": {
        "name": "Study Buddy",
        "icon": "📚",
        "system_prompt": "You are a supportive study buddy. Help users understand concepts, break down complex topics, provide explanations with examples, and encourage learning. Use a friendly and patient tone.",
        "description": "Your learning companion for understanding any subject."
    },
    "Fitness Coach": {
        "name": "Fitness Coach",
        "icon": "💪",
        "system_prompt": "You are an enthusiastic fitness coach. Provide workout advice, nutrition tips, motivation, and guidance on healthy living. Be encouraging and supportive while emphasizing safety and proper form.",
        "description": "Your personal fitness and wellness motivator."
    },
    "Gaming Helper": {
        "name": "Gaming Helper",
        "icon": "🎮",
        "system_prompt": "You are a knowledgeable gaming companion. Help with game strategies, tips, walkthroughs, and gaming news. Use gaming terminology and be enthusiastic about gaming culture.",
        "description": "Your go-to guide for gaming tips and strategies."
    }
}

# Page configuration
st.set_page_config(
    page_title="AI Chatbot with Gemini",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.markdown("---")

    # Personality selector
    st.subheader("Choose AI Personality")
    selected_personality = st.selectbox(
        "Select a personality:",
        options=list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality),
        key="personality_selector"
    )

    # Update personality if changed
    if selected_personality != st.session_state.personality:
        st.session_state.personality = selected_personality
        st.session_state.messages = []  # Clear chat history when personality changes

    # Display personality info
    current_personality = PERSONALITIES[st.session_state.personality]
    st.markdown(f"### {current_personality['icon']} {current_personality['name']}")
    st.info(current_personality['description'])

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### About")
    st.markdown("This chatbot uses Google's Gemini 2.5 Flash model to provide intelligent responses.")
    st.markdown("**Model:** gemini-2.5-flash")

# Main chat interface
st.title(f"{current_personality['icon']} {current_personality['name']}")
st.markdown("Ask me anything!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice input section
st.markdown("### 🎤 Voice Input")
col1, col2 = st.columns([3, 1])

with col1:
    st.info("Click the microphone button to record your voice. After transcription, click 'Send Voice Message' or type your own message below.")

with col2:
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="2x",
    )

# Process audio if recorded
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    # Convert audio to text
    try:
        # Write audio bytes to a temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name

        # Use speech recognition with the audio file
        recognizer = sr.Recognizer()

        with sr.AudioFile(tmp_file_path) as source:
            audio_data = recognizer.record(source)

        with st.spinner("Converting speech to text..."):
            text = recognizer.recognize_google(audio_data)
            st.session_state.voice_text = text
            st.success(f"**Transcribed:** {text}")

        # Clean up temp file
        os.unlink(tmp_file_path)

    except sr.UnknownValueError:
        st.error("Could not understand audio. Please try speaking more clearly.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")

# Use voice text if available, otherwise wait for typed input
if st.session_state.voice_text:
    prompt = st.session_state.voice_text
    st.session_state.voice_text = ""  # Clear after using
elif prompt := st.chat_input("Type your message here...", key="chat_input"):
    pass  # prompt is already set
else:
    prompt = None

st.markdown("---")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Prepare conversation history with system prompt
            conversation_history = [
                {"role": "user", "parts": [current_personality['system_prompt']]},
                {"role": "model", "parts": ["Understood. I will respond according to this personality."]}
            ]

            # Add previous messages
            for msg in st.session_state.messages[:-1]:  # Exclude the last message (current prompt)
                role = "user" if msg["role"] == "user" else "model"
                conversation_history.append({"role": role, "parts": [msg["content"]]})

            # Add current prompt
            conversation_history.append({"role": "user", "parts": [prompt]})

            # Start chat session
            chat = model.start_chat(history=conversation_history[:-1])

            # Get response
            response = chat.send_message(prompt)
            full_response = response.text

            # Display response
            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_message = f"Error: {str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.markdown("Powered by Google Gemini 2.5 Flash | Built with Streamlit")
