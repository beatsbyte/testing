# Custom parser for .properties file
def read_properties(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  # Ignore empty lines and comments
                key, value = line.split('=', 1)
                properties[key.strip()] = value.strip()
    return properties

# Read and use the properties
properties = read_properties('test.properties')

duration_min = int(properties['duration_min'])
duration_max = int(properties['duration_max'])
cnt_music = int(properties['cnt_music'])
request_count = int(properties['request_count'])

# Print fields
print("Duration Min:", duration_min)
print("Duration Max:", duration_max)
print("Count Music:", cnt_music)
print("Request Count:", request_count)
