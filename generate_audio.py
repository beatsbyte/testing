import numpy as np
import random
from pydub import AudioSegment
from pydub.generators import Sine
from test_properties import duration_min, duration_max, cnt_music

# Parameters
sample_rate = 44100  # Standard sample rate (Hz)
output_dir = "./data/"  # Directory to save audio files

# Ensure the output directory exists
import os
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to generate and save audio with multiple sounds
def generate_audio_with_varied_sounds(filename, total_duration_seconds, sound_count):
    combined_audio = AudioSegment.silent(duration=0)  # Start with silent audio
    
    for _ in range(sound_count):
        # Randomize parameters for each sound segment
        duration_seconds = random.randint(2, 5)  # Duration for each sound (2-5 seconds to fill total duration)
        frequency = random.uniform(200, 800)      # Random frequency between 200 Hz and 800 Hz
        amplitude = random.randint(-20, 0)        # Random amplitude (volume in dBFS)
        stereo_effect = random.choice([True, False])  # Add stereo panning effect randomly

        # Generate sine wave
        sine_wave = Sine(frequency, sample_rate=sample_rate).to_audio_segment(
            duration=duration_seconds * 1000,  # Duration in ms
            volume=amplitude
        )
        
        if stereo_effect:
            sine_wave = sine_wave.pan(random.uniform(-1, 1))  # Add stereo effect
        
        # Append this sound to the combined audio
        combined_audio += sine_wave

    # Trim or pad the combined audio to match the total duration
    combined_audio = combined_audio[:total_duration_seconds * 1000]  # Trim to total duration

    # Export the audio file
    output_path = os.path.join(output_dir, filename)
    combined_audio.export(output_path, format="mp3")
    print(f"Generated: {output_path}")

# Generate audio files with random variations and total duration between 10 and 15 seconds
for i in range(cnt_music):
    # Randomize total duration between 10 and 15 seconds
    total_duration_seconds = random.randint(duration_min, duration_max)  # 10 to 15 seconds
    sound_count = random.randint(3, 6)  # Number of different sounds to fill the short duration

    # Generate audio file
    filename = f"audio_{i}.mp3"
    generate_audio_with_varied_sounds(filename, total_duration_seconds, sound_count)
