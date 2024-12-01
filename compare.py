from pydub import AudioSegment
import numpy as np

def load_audio(file_path):
    audio = AudioSegment.from_wav(file_path).set_channels(1)
    return np.array(audio.get_array_of_samples())

def compare_audios(file1, file2):
    audio1 = load_audio(file1)
    audio2 = load_audio(file2)

    min_len = min(len(audio1), len(audio2))
    audio1 = audio1[:min_len]
    audio2 = audio2[:min_len]

    correlation = np.corrcoef(audio1, audio2)[0, 1]
    return correlation

# Load MP3 and OGG files
mp3_audio = AudioSegment.from_file("static/winter-reduced-bitrate.mp3", format="mp3")
ogg_audio = AudioSegment.from_file("static/winter.ogg", format="ogg")

# Export to WAV (common format)
mp3_audio.export("mp3_to_wav.wav", format="wav")
ogg_audio.export("ogg_to_wav.wav", format="wav")

# Compare the two WAV files
audio_file1 = 'mp3_to_wav.wav'
audio_file2 = 'ogg_to_wav.wav'
correlation = compare_audios(audio_file1, audio_file2)
print(f"Коэффициент корреляции: {abs(correlation * 100):.2f}%")
