import os
import sys
import json
import datetime
import speech_recognition as sr
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.wav")


def record_audio():
    
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(OUTPUT_FILENAME, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    return "Запись завершена."


def recognize_audio():
    recognizer = sr.Recognizer()
    with sr.AudioFile(OUTPUT_FILENAME) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio, language="ru-RU")
    except sr.UnknownValueError:
        return "Не удалось распознать речь"
    except sr.RequestError as e:
        return f"Ошибка сервиса распознавания: {e}"


def process_command(cmd):
    if "start" in cmd:
        print(json.dumps({"response": "Запись началась..."}))
        sys.stdout.flush()
        record_audio()
        return recognize_audio()
    elif "stop" in cmd:
        return "Остановлено"
    else:
        return "Пожалуйста, попробуйте ещё раз"

if __name__ == "__main__":
    for line in sys.stdin:
        try:
            data = json.loads(line)
            command = data.get("command", "")

            if not isinstance(command, str):
                command = str(command)

            result = process_command(command)

            print(json.dumps({"response": result}))
            sys.stdout.flush()

        except Exception as e:
            print(json.dumps({"response": f"ERROR: {str(e)}"}))
            sys.stdout.flush()