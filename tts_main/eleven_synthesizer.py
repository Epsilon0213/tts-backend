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


def eleven_tts(speaker_voice, text, output_file):

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
    
    basename, extension = os.path.splitext(output_file)
    output_file_new = basename + ".mp3"

    save_audio_from_bytes(response.content, output_file_new)

    return output_file_new



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



