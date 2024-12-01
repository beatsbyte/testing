# test_audio.py
import numpy as np
import pytest

def test_audio_comparison(load_audio, compare_audio):
    audio_file1 = "static/winter-original.mp3"  # change it to the path of the original audio file
    audio_file2 = "static/winter.ogg"           # change it to the path of the compressed audio file
    
    np_array1, np_array2 = load_audio(audio_file1, audio_file2)

    correlation = compare_audio(np_array1, np_array2)

    print(f"Коэффициент корреляции: {correlation:.2f}%")

    # Assert that the correlation is above a certain threshold
    assert correlation > 85  # Adjust the threshold as needed

def test_audio_comparison_fail(load_audio, compare_audio):
    audio_file1 = "static/winter-original.mp3" # change it to the path of the original audio file
    audio_file2 = "static/compressed.ogg"      # change it to the path of the compressed audio file

    np_array1, np_array2 = load_audio(audio_file1, audio_file2)

    correlation = compare_audio(np_array1, np_array2)
    
    # Assert that the correlation is below a certain threshold
    assert correlation < 50  # Adjust the threshold as needed

