import sounddevice as sd
from scipy.io.wavfile import write

def record_audio():
    freq = 48000
    duration = 5

    recording = sd.rec(int(duration * freq), samplerate = freq, channels = 2)

    sd.wait()
    write("recording.wav", freq, recording)
