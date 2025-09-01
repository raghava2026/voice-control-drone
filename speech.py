# speech_vosk.py
import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

# Load the Vosk model (change path to your model folder)
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

# Queue for audio data
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

# Start listening to microphone
print("🎙 Speak into the microphone...")
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    while True:
        data = q.get()
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")
            if text:
                print(text)
                # Example: exit condition
                if "stop" in text.lower():
                    print("🛑 Stopping listener.")
                    break
        else:
            partial = json.loads(recognizer.PartialResult())
            # print("Partial:", partial)  # Uncomment for real-time feedback

