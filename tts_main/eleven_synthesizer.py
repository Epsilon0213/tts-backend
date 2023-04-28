import requests
import json
import os
import glob
import pygame
import time
from pydub import AudioSegment
import io
from pydub.playback import play
import playsound
import wave


# Replace this with your API key
api_key = "7f3e81b4fd21d6e4b832f16464492017"

# Eleven Labs API endpoint URL
api_endpoint = "https://api.elevenlabs.io/v1/text-to-speech/"


def retrieve_speakers():
    get_speaker_api_endpoint = "https://api.elevenlabs.io/v1/voices"

    headers = {
    "xi-api-key": api_key,
    'Content-Type': 'application/json'
    }

    response = requests.get(get_speaker_api_endpoint, headers=headers)
    voices = json.loads(response.content)
    
    for voice in voices['voices']:
        print(voice['name'], voice['voice_id'])

# retrieve_speakers()


def eleven_tts(speaker_voice, text):

    if speaker_voice == "morgan-freeman":
        speaker_id = "mHOgoY94v8zmhqcKNCOH"

    elif speaker_voice == "david-attenborough":
        speaker_id = "dj4fEDvuyhlVBaB2Qo5E"

    elif speaker_voice == "ellen-degeneres":
        speaker_id = "qSeUanHgscVG9QAaQBRK"

    api_endpoint_speaker = api_endpoint + speaker_id
    print(api_endpoint_speaker)

    headers = {
    "xi-api-key": api_key,
    'Content-Type': 'application/json'
    }

    body = {"text": text,
            "voice_settings": {"stability": 0.75, "similarity_boost": 0.75}
        }
    
    response = requests.post(api_endpoint_speaker, headers=headers, json=body)
    print(response)

    if response.status_code == 200:
        print("Request success! Saving the synthesized audio...")
    else:
        print("API call unsucessful.")
        return

    # Output directory
    outdir = "eleven_synthesis/tts_commercial_history/"

    # Find existing files with the desired naming pattern
    existing_files = glob.glob(os.path.join(outdir, f"tts_{speaker_voice}_*.mp3"))

    # Determine the next file number for the current speaker voice
    file_number = max([int(os.path.splitext(os.path.basename(f))[0].split("_")[2]) for f in existing_files], default=0) + 1

    # Create a new filename with the next available number
    filename = f"tts_{speaker_voice}_{file_number}.mp3"
    out_dest = os.path.join(outdir, filename)

    save_audio_from_bytes(response.content, out_dest)
    play_audio(out_dest)



def save_audio_from_bytes(data, output_file):

    with open(output_file, 'wb') as output_file:
        output_file.write(data)



def play_audio(file):

    pygame.init()
    pygame.mixer.init(frequency=44100, channels=1, devicename='CABLE Input (VB-Audio Virtual Cable)')

    # Construct the file path based on the content parameter
    audio_file = f"{file}"

    try:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
    except FileNotFoundError:
        print(f"Audio file {audio_file} not found")



