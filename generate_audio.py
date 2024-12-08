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
    
    remaining_duration = total_duration_seconds * 1000  # Convert total duration to milliseconds
    for i in range(sound_count):
        if i == sound_count - 1:  # Last sound fills the remaining duration
            duration_ms = remaining_duration
        else:
            # Divide remaining duration randomly among remaining sounds
            avg_duration = remaining_duration / (sound_count - i)
            duration_ms = random.randint(int(avg_duration * 0.8), int(avg_duration * 1.2))
            duration_ms = min(duration_ms, remaining_duration)  # Ensure it doesn't exceed remaining duration
        
        remaining_duration -= duration_ms  # Reduce remaining duration

        # Randomize parameters for each sound segment
        frequency = random.uniform(200, 800)      # Random frequency between 200 Hz and 800 Hz
        amplitude = random.randint(-20, 0)        # Random amplitude (volume in dBFS)
        stereo_effect = random.choice([True, False])  # Add stereo panning effect randomly

        # Generate sine wave
        sine_wave = Sine(frequency, sample_rate=sample_rate).to_audio_segment(
            duration=duration_ms,  # Duration in ms
            volume=amplitude
        )
        
        if stereo_effect:
            sine_wave = sine_wave.pan(random.uniform(-1, 1))  # Add stereo effect
        
        # Append this sound to the combined audio
        combined_audio += sine_wave

    # Ensure the combined audio is exactly the specified duration
    combined_audio = combined_audio[:total_duration_seconds * 1000]  # Trim to total duration

    # Export the audio file
    output_path = os.path.join(output_dir, filename)
    combined_audio.export(output_path, format="mp3")
    print(f"Generated: {output_path}")

# Generate audio files with random variations and total duration between 10 and 15 seconds
for i in range(cnt_music):
    # Randomize total duration between duration_min and duration_max
    total_duration_seconds = random.randint(duration_min, duration_max)
    sound_count = random.randint(3, 6)  # Number of different sounds to fill the duration

    # Generate audio file
    filename = f"audio_{i}.mp3"
    generate_audio_with_varied_sounds(filename, total_duration_seconds, sound_count)
