from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os

load_dotenv()

client = ElevenLabs(api_key=os.getenv("TTS_API_KEY"))

mario_voice_id = "tomkxGQGz4b1kE0EM722"
lina_voice_id = "VmejBeYhbrcTPwDniox7"
july_voice_id = "MD6rLAhozcrmkdMZeOBt"

text = "Ella es responsable de coordinar el proyecto."

print("Generating audio...")
audio = client.text_to_speech.convert(
    text=text,
    voice_id=mario_voice_id,
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

file_name = "output3.mp3"
save(audio, file_name)
print(f"Saved to {file_name}")
