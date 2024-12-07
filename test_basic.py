import pytest
from aiohttp.payload import BytesPayload
import aiohttp
import os
url = "http://192.168.0.60:8080"
file_path = "data/test_input.mp3"
async def test_send_music(send_music):
    output_file_path = await send_music(url, file_path)
    assert os.path.exists(output_file_path)


async def test_check_audio(send_music, audio2npArray, compare_audio):
    output_file_path = await send_music(url, file_path)
    np_array1 = audio2npArray(file_path)
    np_array2 = audio2npArray(output_file_path)
    correlation = compare_audio(np_array1, np_array2)
    assert correlation > 85

async def test_service_alive():
    async with aiohttp.ClientSession() as session:
        async with session.put(f'{url}/v1/imalive', json={'url': 'v1/compress'}) as response:
            assert response.status == 200

def test_basic():
    assert 1 == 1

