import asyncio
import time
import aiohttp
from aiohttp.payload import BytesPayload, StringPayload
from random import randint
from test_properties import*

# Define the server URL and file path
url = "http://192.168.0.60:8080"
file_path = "data/"

def number_sequence():
    count = 1
    while True:
        yield str(count)
        count += 1

seq = number_sequence()

async def send_music(url, file_path, id):
    print(f"Sending request {id}...")
    try:
        # Open the file based on the generated random file name
        with open(file_path, "rb") as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False

    # Prepare the multipart form-data payload
    with aiohttp.MultipartWriter() as data:
        payload = BytesPayload(
            file_content,
            content_type="audio/mpeg",
            filename=f"audio_{id}.mp3"
        )
        part = data.append_payload(payload)
        part.set_content_disposition('form-data', name='file', filename=f"audio_{id}.mp3")

        payload_compress_degree = StringPayload(
            str(compress_degree),
            content_type="text/plain",
        )
        part = data.append_payload(payload_compress_degree)
        part.set_content_disposition('form-data', name='compress_degree')

    headers = {
        "Content-Type": f"multipart/form-data; boundary={data.boundary}",
    }

    is_success = True

    # Make the HTTP POST request
    async with aiohttp.ClientSession() as session:
        # dic = {}
        try:
            async with session.post(f'{url}/v1/compress', data=data, headers=headers) as response:
                if response.status != 200:
                    is_success = False
                    print(f"Request {id} failed with status: {response.status}")
                else:
                    ogg_content = await response.read()
                    output_file_path = f"data/test_output_{id}.ogg"
                    with open(output_file_path, "wb") as output_file:
                        output_file.write(ogg_content)
                    print(f"Request {id} completed. Output saved to {output_file_path},{response.headers["X-Proxy-Worker-Url"]}")
                    # if response.headers["X-Proxy-Worker-Url"] not in dic:
                        # dic[response.headers["X-Proxy-Worker-Url"]] = 0
                    # dic[response.headers["X-Proxy-Worker-Url"]] += 1

        except Exception as e:
            is_success = False
            print(f"Request {id} failed: {e}")
    # print(dic)
    return is_success

async def test_concurrent_requests(num_requests):
    # Measure the time
    start_time = time.time()
    
    # Create tasks for all requests
    tasks = [
        send_music(url, f"data/audio_{randint(0, cnt_music-1)}.mp3", next(seq))
        for _ in range(num_requests)
    ]
    
    # Run all tasks concurrently
    responses = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    # Print the results
    print(f"Time taken for all requests: {end_time - start_time:.2f} seconds")
    print(f"Number of successful requests: {sum(responses)}")
    print(f"Number of failed requests: {num_requests - sum(responses)}")

# Run the test with the specified number of requests
asyncio.run(test_concurrent_requests(request_count))
