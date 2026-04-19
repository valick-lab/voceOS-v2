from email.mime import text
import os
import sys
import json
import datetime
import speech_recognition as sr
import pyaudio
import wave
import threading
import time
from commands import hello
from core.handle import handle


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.wav")
stats = False
loop_event = threading.Event()


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
    # работа в .wav файлами. задумка - сделать 'конструктор команд'
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
    global stats
    normalized = str(cmd).strip().lower()
    if "start" in normalized:
        if stats:
            return "Цикл записи уже запущен", None
        stats = True
        loop_event.set()
        return "Запись началась", "Listening"
    elif "stop" in normalized:
        if not stats:
            return "Цикл записи уже остановлен", None
        stats = False
        loop_event.clear()
        return "Остановлено", "Idle"
    else:
        return "Пожалуйста, попробуйте ещё раз", None


def command_reader():
    for line in sys.stdin:
        try:
            data = json.loads(line)
            command = data.get("command", "")
            result, status = process_command(command)
            payload = {"response": result}
            if status:
                payload["status"] = status
            print(json.dumps(payload))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"response": f"ERROR: {str(e)}"}))
            sys.stdout.flush()
    loop_event.clear()


def recording_loop():
    
    while True:
        loop_event.wait()
        if not stats:
            continue

        record_audio()
        print(json.dumps({"status": "Thinking"}))
        sys.stdout.flush()

        text = recognize_audio()
        response = handle(text)

        payload = {"response": response if response else text}
        payload["status"] = "Listening" if stats else "Idle"
        print(json.dumps(payload))
        sys.stdout.flush()

        if not stats:
            continue
        time.sleep(0.1)


if __name__ == "__main__":
    thread = threading.Thread(target=command_reader, daemon=True)
    thread.start()
    recording_loop()
