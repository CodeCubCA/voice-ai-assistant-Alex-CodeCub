# Voice AI Assistant - Streamlit Chatbot

A voice-enabled AI chatbot application built with Streamlit and Google Gemini API, featuring speech-to-text input, text-to-speech output, and multiple AI personalities.

## Features

- 🤖 **AI-Powered Chat**: Powered by Google Gemini 2.5 Flash model
- 🎤 **Voice Input**: Record your voice and get automatic speech-to-text conversion
- 🔊 **Voice Output**: Text-to-speech (TTS) for AI responses with automatic audio generation
- 🎭 **Multiple Personalities**: Choose from 4 different AI personalities:
  - General Assistant - Versatile helper for various topics
  - Study Buddy - Patient learning companion
  - Fitness Coach - Motivational fitness and wellness guide
  - Gaming Helper - Knowledgeable gaming companion
- 💬 **Chat History**: Maintains conversation context throughout the session
- ⌨️ **Dual Input**: Support for both voice and text input
- 🎨 **Clean UI**: User-friendly interface with polished layout and helpful feedback

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key (get yours at [Google AI Studio](https://aistudio.google.com/app/apikey))
- Microphone (for voice input feature)
- Internet connection (for speech recognition and AI responses)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CodeCubCA/voice-ai-assistant-Alex-CodeCub.git
   cd voice-ai-assistant-Alex-CodeCub
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**

   Open your browser and navigate to:
   - Local URL: `http://localhost:8501`
   - Network URL: `http://your-ip:8501`

3. **Using Voice Input**
   - Click the microphone button to start recording
   - Speak clearly into your microphone
   - Click the button again to stop recording
   - The audio will be automatically transcribed and sent to the AI

4. **Using Text Input**
   - Type your message in the text input box at the bottom
   - Press Enter to send

5. **Listening to AI Responses**
   - Audio is automatically generated for each AI response
   - Audio player appears below each assistant message with a divider
   - Use browser controls to play, pause, adjust speed, or control volume
   - Long messages may take a moment to generate audio

6. **Switching Personalities**
   - Use the sidebar to select different AI personalities
   - Chat history will be cleared when switching personalities

## Project Structure

```
voice-ai-assistant/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your API keys (git-ignored)
├── .gitignore           # Git ignore configuration
└── README.md            # This file
```

## Dependencies

- `streamlit>=1.31.0` - Web framework for the UI
- `google-generativeai>=0.3.2` - Google Gemini API client
- `python-dotenv>=1.0.0` - Environment variable management
- `audio-recorder-streamlit>=0.0.8` - Audio recording component
- `SpeechRecognition>=3.10.0` - Speech-to-text conversion
- `gtts>=2.3.0` - Google Text-to-Speech for audio output

## Technical Details

### Voice Recognition Implementation

The voice input feature uses a two-step process to ensure reliable speech recognition:

1. **Audio Recording**: Uses `audio-recorder-streamlit` to capture audio from the microphone
2. **Speech-to-Text**: Converts audio to text using Google Speech Recognition API
   - Audio is saved to a temporary WAV file
   - `sr.AudioFile()` is used to properly handle audio format
   - This approach ensures correct sample rate and audio format parsing

**Important Note**: The implementation uses `sr.AudioFile()` instead of `sr.AudioData()` constructor to avoid format compatibility issues.

### Text-to-Speech Implementation

The TTS feature provides automatic audio generation for AI responses:

1. **Automatic Generation**: Every AI response is automatically converted to speech
2. **Audio Playback**: Audio players are displayed below each AI message with playback controls
3. **Smart Features**:
   - Warning alerts for long messages that may take time to process
   - Automatic truncation for extremely long messages (>1000 characters)
   - Browser-native playback controls (play, pause, speed adjustment, volume)
   - Graceful error handling - chat continues even if audio generation fails
4. **Implementation Details**:
   - Uses Google Text-to-Speech (gTTS) library
   - Audio saved as temporary MP3 files
   - Audio players rendered outside chat message containers for Streamlit compatibility
   - Anti-loop protections prevent duplicate audio generation

### AI Model

- **Model**: Google Gemini 2.5 Flash (`gemini-2.5-flash`)
- **Context**: Maintains conversation history with system prompts
- **Personalities**: Each personality has a custom system prompt that influences AI behavior

## Configuration

### Customizing AI Personalities

Edit the `PERSONALITIES` dictionary in `app.py` to add or modify personalities:

```python
PERSONALITIES = {
    "Your Personality Name": {
        "name": "Display Name",
        "icon": "🎯",
        "system_prompt": "Your custom system prompt here...",
        "description": "Brief description"
    }
}
```

### Adjusting UI Colors

Modify the `audio_recorder` parameters in `app.py`:

```python
audio_bytes = audio_recorder(
    recording_color="#e74c3c",  # Color when recording
    neutral_color="#3498db",    # Color when idle
    icon_name="microphone",
    icon_size="2x",
)
```

## Troubleshooting

### Voice Recognition Issues

**Problem**: "Could not understand audio" error

**Solutions**:
- Speak more clearly and at a moderate pace
- Reduce background noise
- Check your microphone is working properly
- Ensure you have a stable internet connection

**Problem**: Audio processing fails

**Solutions**:
- Verify the `SpeechRecognition` library is properly installed
- Check that temporary files can be created in your system
- Ensure Google Speech Recognition API is accessible

### Text-to-Speech Issues

**Problem**: Audio not generating for AI responses

**Solutions**:
- Check that `gtts` library is properly installed
- Verify internet connection (gTTS requires online access)
- Check browser console for any errors
- Ensure temporary files can be created in your system

**Problem**: Audio playback not working

**Solutions**:
- Try a different browser (Chrome, Firefox, Edge recommended)
- Check browser audio/autoplay settings
- Verify system volume is not muted
- Try refreshing the page

### API Issues

**Problem**: API key errors

**Solutions**:
- Verify your `.env` file exists and contains the correct API key
- Check that your Gemini API key is valid
- Ensure you haven't exceeded API rate limits

**Problem**: Gemini model errors

**Solutions**:
- Confirm you're using the correct model name: `gemini-2.5-flash`
- Check your internet connection
- Verify your API key has access to the Gemini API

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and private
- The `.gitignore` file is configured to exclude `.env` automatically
- Use `.env.example` as a template for other users

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is for educational purposes.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini API](https://ai.google.dev/)
- Speech recognition by [Google Speech Recognition](https://cloud.google.com/speech-to-text)
- Text-to-speech by [gTTS (Google Text-to-Speech)](https://github.com/pndurette/gTTS)
- Audio recording component by [audio-recorder-streamlit](https://github.com/Joooohan/audio-recorder-streamlit)

## Author

Created as part of CodeCub's AI development course.

---

**Powered by Google Gemini 2.5 Flash | Built with Streamlit**
