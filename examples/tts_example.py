import os

import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

openai.api_key = OPENAI_API_KEY

def text_to_speech(text: str, output_file: str = "output.mp3", voice: str = "alloy"):
    """
    Convert text to speech using OpenAI's TTS API
    
    Args:
        text: Text to convert to speech
        output_file: Path where to save the audio file
        voice: Voice to use (alloy, echo, fable, onyx, nova, or shimmer)
    """
    try:
        # Generate speech from text
        response = openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=voice,
            input=text
        )
        
        # Save to file
        with open(output_file, "wb") as audio_file:
            audio_file.write(response.content)
        
        print(f"Audio saved to {output_file}")
        
    except Exception as e:
        print(f"Error generating speech: {e}")

if __name__ == "__main__":
    # Example usage
    example_text = "Hi! This is a test of the OpenAI TTS API."
    text_to_speech(example_text, "test_tts_output.mp3")