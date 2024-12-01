# conftest.py
import pytest
from pydub import AudioSegment
import numpy as np

@pytest.fixture
def load_audio(request):
    def _load_audio(file_path1, file_path2):
        audio1 = AudioSegment.from_file(file_path1)
        audio1.export("mp3_to_wav.wav", format="wav")
        audio1 = AudioSegment.from_wav("mp3_to_wav.wav").set_channels(1)

        audio2 = AudioSegment.from_file(file_path2)
        audio2.export("ogg_to_wav.wav", format="wav")
        audio2 = AudioSegment.from_wav("ogg_to_wav.wav").set_channels(1)


        return np.array(audio1.get_array_of_samples()), np.array(audio2.get_array_of_samples())
    
    return _load_audio

@pytest.fixture
def compare_audio():
    def _compare_audio(np_array1, np_array2):
        min_len = min(len(np_array1), len(np_array2))
        np_array1 = np_array1[:min_len]
        np_array2 = np_array2[:min_len]
        
        correlation = np.corrcoef(np_array1, np_array2)[0, 1]
        correlation = max(correlation, 0)
        return correlation * 100

    return _compare_audio