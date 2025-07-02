from pathlib import Path
from openai import OpenAI

voices = {
    "male": ["ash", "onyx"],
    "female": ["coral", "shimmer"]
}

voice = voices["male"][1]  

filename = f"{voice}"

client = OpenAI()
speech_dir = Path(__file__).parent / "voices"
speech_dir.mkdir(parents=True, exist_ok=True)
speech_file_path = speech_dir / f"{filename}.mp3"

instructions=(
        "Acento: español de Colombia neutro. "
        "Tono: neutro. "
        "Velocidad: un 10 % más lenta de lo normal. "
        "Pronunciación: clara, marcando las consonantes."
        )


with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice=voice,
    input="soy",
    instructions=instructions
) as response:
    response.stream_to_file(speech_file_path)

print(instructions)