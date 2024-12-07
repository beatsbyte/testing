import pytest
from aiohttp.payload import BytesPayload
import aiohttp
import os

async def test_send_music(service_client, send_music):
    file_path = "data/test_input.mp3"
    output_file_path = await send_music(file_path)
    assert os.path.exists(output_file_path)


async def test_check_audio(service_client, send_music, audio2npArray, compare_audio):
    file_path = "data/test_input.mp3"
    output_file_path = await send_music(file_path)
    np_array1 = audio2npArray(file_path)
    np_array2 = audio2npArray(output_file_path)
    correlation = compare_audio(np_array1, np_array2)
    assert correlation > 85


def test_basic():
    assert 1 == 1

