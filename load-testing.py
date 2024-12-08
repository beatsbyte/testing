import asyncio
import time
import sys
from conftest import send_music
import aiohttp
from aiohttp.payload import BytesPayload
import pytest
from random import randint
url = "http://192.168.0.61:8080"
file_path = "data/test_input.mp3"

def number_sequence():
    count = 1
    while True:
        yield str(count)
        count += 1
seq = number_sequence()

async def send_music(url, file_path, id):
    print(f"Sending request {id}...")
    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
    except FileNotFoundError:
        pass


    with aiohttp.MultipartWriter() as data:
        payload = BytesPayload(
            file_content,
            content_type="audio/mpeg",
            filename="test_input.mp3"
        )

        part = data.append_payload(payload)
        part.set_content_disposition('form-data', name='file', filename="test_input.mp3")

    headers = {
        "Content-Type": f"multipart/form-data; boundary={data.boundary}",
    }

    is_success = True

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f'{url}/v1/compress', data=data, headers=headers) as response:
                if response.status != 200:
                    is_success = False
                    print(f"Request {id} failed with status: {response.status}")
                else:
                    ogg_content = await response.read()
                    print(f"Request {id} completed")
        except Exception as e:
            is_success = False
            print(f"Request {id} failed: {e}")

    return is_success
    # ogg_content = await response.read()
    # output_file_path = f"data/test_output_{id}.ogg"
    # with open(output_file_path, "wb") as output_file:
    #     output_file.write(ogg_content)
    
    # return output_file_path
    


# Test function
async def test_concurrent_requests(num_requests):
    # num_requests = 10  # Number of requests to send concurrently
    
    # Measure the time
    start_time = time.time()
    
    # Create tasks for all requests
    tasks = []
    for i in range(num_requests):
        file_path = f"data/audio_{randint(0, 99)}.mp3"
        tasks.append(send_music(url, file_path, next(seq)))
    # tasks = [send_music(url, file_path, next(seq)) for _ in range(num_requests)]
    
    # Run all tasks concurrently
    responses = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    # Assertions
    # assert len(responses) == num_requests  # Ensure we get responses for all requests
    
    print(f"Time taken for all requests: {end_time - start_time:.2f} seconds")
    print(f"Number of successful requests: {sum(responses)}")
    print(f"Number of failed requests: {num_requests - sum(responses)}")

num_requests = int(sys.argv[1])

asyncio.run(test_concurrent_requests(num_requests))
# test_concurrent_requests()