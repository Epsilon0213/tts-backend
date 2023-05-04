import pyttsx3
import tempfile
from pydub import AudioSegment
import soundfile as sf
import sounddevice as sd
import pyaudio
import wave
import pygame
import time
import os
import sys
from corentinj_synthesizer import corentinj_tts
from eleven_synthesizer import eleven_tts
from scipy.signal import butter, filtfilt
import librosa
import time
import hashlib
from datetime import datetime
from playsound import playsound




class soundEngine():

    def __init__(self):
        self.model = "robotic"
        self.voice = "morgan-freeman"
        self.voice_properties = {
            "morgan-freeman": {"pitch": -7, "rate": 140, "voice_id": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"},
            "david-attenborough": {"pitch": -3, "rate": 140, "voice_id": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"},
            "ellen-degeneres": {"pitch": -5, "rate": 180, "voice_id": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"},
        }
    
    def voice_select(self, content):
        self.voice = content
        print("voice selected is: ", content)
    
    def model_select(self, content):
        self.model = content
        print("model selected is: ", content)

    def talk(self, content):

        # Generate a unique hash ID based on the content
        hash_id = hashlib.sha1(content.encode()).hexdigest()

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create a unique output filename with the hash ID
        outdir = "tts_main/tts_output/"
        output_filename = f"{self.model}_{self.voice}{timestamp}_{hash_id}.wav"
        output_file = os.path.join(outdir, output_filename)


        if (self.model == "robotic"):
            print("Synthesizing new audio with pyttsx3...")
            engine = pyttsx3.Engine()
            engine.save_to_file(content, output_file)
            engine.runAndWait()
        
        elif (self.model == "simple_clone"):
            print("Synthesizing speech with pyttx3 and LPF")

            voice_properties = self.voice_properties[self.voice]
            pitch_value = voice_properties["pitch"]

            ps_content = f'<pitch middle="{pitch_value}">{content}</pitch>'

            engine = pyttsx3.Engine()
            engine.setProperty('voice', voice_properties["voice_id"])
            engine.setProperty('rate', voice_properties["rate"])

            buffer_output_file = os.path.join(outdir, f"{self.model}_buffer_{self.voice}_{hash_id}.wav")

            engine.save_to_file(ps_content, buffer_output_file)
            engine.runAndWait()
            self.lpf(buffer_output_file, output_file)



        elif (self.model == "ai_clone"):
            print("Synthesizing speech with CorentinJ")
            corentinj_tts(self.voice, content, output_file)

        elif (self.model == "commercial"):
            print("Synthesizing speech with ElevenLabs")
            mp3_output_file = eleven_tts(self.voice, content, output_file)

        # Playing the audio
        if(self.model != "commercial"):
            play_file = output_file
        else:
            play_file = mp3_output_file
    
       # self.load_and_play_synthesis(play_file)
        
        raw_filename = play_file.split('/')
        # ['tts_main', 'tts_output', 'robotic_morgan-freeman20230504225142_94dd9e08c129c785f7f256e82fbe0a30e6d1ae40.wav']
        return "", raw_filename[2]
        

    def load_and_play_synthesis(self, file):

        pygame.init()
        pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()
        except FileNotFoundError:
            print(f"Audio file {file} not found")

        
    def play_effect(self, content):

        # pygame.init()
        # pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

        # Construct the file path based on the content parameter
        audio_file = f"tts_main/sounds/effects/{content}.wav"
        raw_filename = audio_file.split('/')

        # try:
        #     pygame.mixer.music.load(audio_file)
        #     pygame.mixer.music.play()
        #     while pygame.mixer.music.get_busy():
        #         time.sleep(0.1)
        # except FileNotFoundError:
        #     print(f"Audio file {audio_file} not found")

        return "", raw_filename[3]


            
    
    def speak_phrase(self, content):

        # pygame.init()
        # pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

        # # Construct the file path based on the content parameter
        audio_file = f"tts_main/sounds/phrases/{self.voice}-{content}.wav"
        raw_filename = audio_file.split('/')


        # try:
        #     pygame.mixer.music.load(audio_file)
        #     pygame.mixer.music.play()
        #     while pygame.mixer.music.get_busy():
        #         time.sleep(0.1)
        # except FileNotFoundError:
        #     print(f"Audio file {audio_file} not found")\

        return "", raw_filename[3]

            


    def play_music(self, content):
        
        pygame.init()
        pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

        # Construct the file path based on the content parameter
        audio_file = f"tts_main/sounds/music/{content}.mp3"

        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops=-1)
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except FileNotFoundError:
            print(f"Audio file {audio_file} not found")


    def stop_music(self, content):

        pygame.init()
        pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
        pygame.mixer.music.stop()

    
    def lpf(self, audio_file, output_file):
        y, sr = librosa.load(audio_file)
        cutoff_hz = 2000

        # Define the filter
        nyquist_rate = sr / 2.0
        b, a = butter(5, cutoff_hz / nyquist_rate, btype="low")

        # Apply the filter
        y_filtered = filtfilt(b, a, y)

        sf.write(output_file, y_filtered, sr)

        
