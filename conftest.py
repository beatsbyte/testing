# conftest.py
import pytest
from pydub import AudioSegment
import numpy as np
import os
import aiohttp
import asyncio

@pytest.fixture
async def send_music(service_client):
    async def _send_music(file_path):
        try:
            with open(file_path, "rb") as file:
                file_content = file.read()
        except FileNotFoundError:
            pytest.fail(f"Test MP3 file not found: {file_path}")


        with aiohttp.MultipartWriter() as data:
            payload = BytesPayload(
                file_content,
                content_type="audio/mpeg",
                filename="test_input.mp3"
            )

            part = data.append_payload(payload)
            part.set_content_disposition('form-data', name='file', filename="data/test_input.mp3")

        headers = {
            "Content-Type": f"multipart/form-data; boundary={data.boundary}",
        }

        response = await service_client.post(
            '/convert-to-ogg',
            data=data,
            headers=headers
        )

        content_type = response.headers.get("Content-Type", "")

        ogg_content = await response.read()
        output_file_path = "data/test_output.ogg"
        with open(output_file_path, "wb") as output_file:
            output_file.write(ogg_content)
        
        return output_file_path
    
    return _send_music



@pytest.fixture
def audio2npArray():
    def _audio2npArray(audio_path):
        audio = AudioSegment.from_file(audio_path)
        audio_common_type = ".build/audio.wav"
        audio.export(audio_common_type, format="wav")
        audio = AudioSegment.from_wav(audio_common_type).set_channels(1)
        return np.array(audio.get_array_of_samples())
    return _audio2npArray

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