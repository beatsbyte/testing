import pytest
from aiohttp.payload import BytesPayload
import aiohttp
import os
import logging
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("URL")

async def test_send_music_easy(send_music, send_music_list):
    response = await send_music_list("temp", 0)
    total_size, total_compressed_size = response
    print(f"easy: {total_size} KB -> {total_compressed_size} KB")

async def test_send_music_medium(send_music, send_music_list):
    response = await send_music_list("temp", 1)
    total_size, total_compressed_size = response
    print(f"medium: {total_size} KB -> {total_compressed_size} KB")

async def test_send_music_hard(send_music, send_music_list):
    response = await send_music_list("temp", 2)
    total_size, total_compressed_size = response
    print(f"hard: {total_size} KB -> {total_compressed_size} KB")


async def test_similarity_easy(send_music, calc_similarity):
    test_path = "music/music1.mp3"
    response_path = "responses/music1_response_easy.mp3"
    response = await send_music(test_path, 0)

    with open(response_path, "wb") as file:
        file.write(await response.read())

    similarity_percentage = await calc_similarity(test_path, response_path)
    print("Easy: ", similarity_percentage)
    assert similarity_percentage >= 85

async def test_similarity_medium(send_music, calc_similarity):
    test_path = "music/music1.mp3"
    response_path = "responses/music1_response_medium.mp3"
    response = await send_music(test_path, 1)
    
    with open(response_path, "wb") as file:
        file.write(await response.read())

    similarity_percentage = await calc_similarity(test_path, response_path)
    print("Medium: ", similarity_percentage)
    assert similarity_percentage >= 70

async def test_similarity_hard(send_music, calc_similarity):
    test_path = "music/music1.mp3"
    response_path = "responses/music1_response_hard.mp3"
    response = await send_music(test_path, 2)

    with open(response_path, "wb") as file:
        file.write(await response.read())

    similarity_percentage = await calc_similarity(test_path, response_path)
    print("Hard: ", similarity_percentage)
    assert similarity_percentage >= 50

async def test_service_alive():
    async with aiohttp.ClientSession() as session:
        async with session.put(f'{url}/v1/imalive', json={'url': 'v1/compress'}) as response:
            assert response.status == 200
            logging.info("Service is alive")

def test_basic():
    assert 1 == 1
