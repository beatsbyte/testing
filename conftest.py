import pytest
from pydub import AudioSegment
import numpy as np
import os
import aiohttp
from aiohttp.payload import BytesPayload, StringPayload
from dotenv import load_dotenv
import logging
from pprint import pprint

load_dotenv()
url = os.getenv("URL")
@pytest.fixture
async def send_music():
    async def _send_music(file_path: str, level: int):
        with open(file_path, "rb") as file:
            file_content = file.read()

        with aiohttp.MultipartWriter() as data:
            file_payload = BytesPayload(
                file_content,
                content_type="audio/mpeg",
                filename=file_path
            )
            
            part = data.append_payload(file_payload)
            part.set_content_disposition('form-data', name='file', filename=file_path)

            level_payload = StringPayload(
                str(level),
                content_type="text/plain"
            )
            part = data.append_payload(level_payload)
            part.set_content_disposition('form-data', name='compress_degree')

        headers = {
            "Content-Type": f"multipart/form-data; boundary={data.boundary}",
        }

        session = aiohttp.ClientSession()
        response = await session.post(f'{url}/v1/compress', data=data, headers=headers)
        return response

    return _send_music

@pytest.fixture
def audio2npArray():
    def _audio2npArray(audio_path):
        audio = AudioSegment.from_mp3(audio_path).set_channels(1)
        return np.array(audio.get_array_of_samples())
    return _audio2npArray

@pytest.fixture
def similarity():
    def _similarity(np_array1, np_array2):
        min_len = min(len(np_array1), len(np_array2))
        np_array1 = np_array1[:min_len]
        np_array2 = np_array2[:min_len]
        
        correlation = np.corrcoef(np_array1, np_array2)[0, 1]
        return abs(correlation) * 100

    return _similarity


@pytest.fixture
def getsize():
    def _getsize(file_path):
        return os.path.getsize(file_path)//1024
    return _getsize

@pytest.fixture
async def send_music_list(send_music, getsize):
    async def _send_music_list(file_paths, level):
        total_size = 0
        total_compressed_size = 0
        for file in os.listdir(file_paths):
            file_path = f"{file_paths}/{file}"
            response = await send_music(file_path, level)

            logging.info(f"Used backend url: {response.headers['X-Proxy-Worker-Url']}")
            response_path = f"responses/{file.split('.')[0]}_response_{level}.mp3"
            with open(response_path, "wb") as file:
                file.write(await response.read())
            
            logging.info(f"Compressed file saved at {response_path}.")
            logging.info(f"Compress result: {getsize(file_path)} KB -> {getsize(response_path)} KB")
            pprint(f"Compress result: {file_path} :: {getsize(file_path)} KB -> {getsize(response_path)} KB")

            total_size += getsize(file_path)
            total_compressed_size += getsize(response_path)

        return total_size, total_compressed_size
    return _send_music_list


@pytest.fixture
async def calc_similarity(audio2npArray, similarity):
    async def _calc_similarity(file_path, response_path):
        file_data = audio2npArray(file_path)
        response_data = audio2npArray(response_path)

        similarity_percentage = similarity(file_data, response_data)
        similarity_percentage = round(similarity_percentage, 2)
        return similarity_percentage
    return _calc_similarity