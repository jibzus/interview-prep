import pyaudio
import wave
import numpy as np
import whisper
import os


class AudioRecorder:
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100, chunk_size=1024, silence_threshold=500,
                 silence_duration=2):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk_size = chunk_size
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.audio_interface = pyaudio.PyAudio()
        self.stream = None

    def is_silence(self, snd_data):
        """Determine if a given chunk is silence."""
        snd_data = np.frombuffer(snd_data, dtype=np.int16)
        return abs(np.mean(snd_data)) < self.silence_threshold

    def record_until_silence(self):
        """Record audio until silence is detected for a specified duration."""
        print("Recording...")
        self.stream = self.audio_interface.open(format=self.format, channels=self.channels,
                                                rate=self.rate, input=True, frames_per_buffer=self.chunk_size)
        frames = []
        silence_frames = 0
        while True:
            data = self.stream.read(self.chunk_size, exception_on_overflow=False)
            frames.append(data)
            if self.is_silence(data):
                silence_frames += 1
                if silence_frames >= self.rate / self.chunk_size * self.silence_duration:
                    break
            else:
                silence_frames = 0

        self.stream.stop_stream()
        self.stream.close()
        return frames

    def save_recording(self, frames, filename="temp.wav"):
        """Save the recorded audio to a file."""
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio_interface.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        return filename

    def close(self):
        """Close PyAudio interface."""
        self.audio_interface.terminate()


def transcribe_audio(filename):
    """Transcribe audio file using Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print("Transcription:", result["text"])
    return result["text"]


if __name__ == "__main__":
    recorder = AudioRecorder()
    try:
        frames = recorder.record_until_silence()
        wav_filename = recorder.save_recording(frames)
        text = transcribe_audio(wav_filename)

        # Save transcription to a text file
        text_filename = 'audio-extraction/tejEats.txt'  #datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_transcription.txt"
        with open(text_filename, 'w') as f:
            f.write(text)
        print(f"Transcription saved to {text_filename}")

        # Optionally, remove the WAV file if it's no longer needed
        os.remove(wav_filename)

    finally:
        recorder.close()