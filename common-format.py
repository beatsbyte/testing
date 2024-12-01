from pydub import AudioSegment

# Load MP3 and OGG files
mp3_audio = AudioSegment.from_file("static/original-reversed.mp3", format="mp3")
ogg_audio = AudioSegment.from_file("static/compressed.ogg", format="ogg")

# Export to WAV (common format)
mp3_audio.export("mp3_to_wav.wav", format="wav")
ogg_audio.export("ogg_to_wav.wav", format="wav")
