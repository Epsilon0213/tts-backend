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
from corentinj_synthesizer import synthesize_speech
from eleven_synthesizer import eleven_tts
from scipy.signal import butter, filtfilt
import librosa
import time



class soundEngine():

    def __init__(self):
        self.model = "robotic"
        self.voice = "morgan-freeman"
        self.voice_properties = {
            "morgan-freeman": {"pitch": -7, "rate": 140, "voice_id": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"},
            "david-attenborough": {"pitch": -3, "rate": 140, "voice_id": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"},
            "ellen-degeneres": {"pitch": -5, "rate": 180, "voice_id": "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"},
        }
        self.index = 1
    
    def voice_select(self, content):
        self.voice = content
        print("voice selected is: ", content)
    
    def model_select(self, content):
        self.model = content
        print("model selected is: ", content)

    def talk(self, content):

        num_words = len(content.split())
        print(f"Number of words in content: {num_words}")
        
        num_characters = len(content)
        print(f"Number of characters in content: {num_characters}")

        start_time = time.time()

        if (self.model == "robotic"):
            print("Synthesizing new audio with pyttsx3...")
            engine = pyttsx3.Engine()
            end_time = time.time()
            engine.say(content)
            engine.runAndWait()
        
        elif (self.model == "simple_clone"):
            print("Synthesizing speech with pyttx3 and LPF")

            voice_properties = self.voice_properties[self.voice]
            pitch_value = voice_properties["pitch"]

            ps_content = f'<pitch middle="{pitch_value}">{content}</pitch>'

            engine = pyttsx3.Engine()
            engine.setProperty('voice', voice_properties["voice_id"])
            engine.setProperty('rate', voice_properties["rate"])


            output_file_name = self.voice.replace('-', '_')
            output_file = f"tts_main/tts_output/simple_clone/{output_file_name}_tts{self.index}.wav"

            engine.save_to_file(ps_content, output_file)
            engine.runAndWait()


            output_lpf_file_name = output_file_name + "_lpf"
            output_lpf_file = f"tts_main/tts_output/simple_clone/{output_lpf_file_name}_tts{self.index}.wav"

            self.lpf(output_file, output_lpf_file)

            pygame.init()
            pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

            try:
                pygame.mixer.music.load(output_lpf_file)
                end_time = time.time()
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                pygame.mixer.music.unload()
            except FileNotFoundError:
                print(f"Audio file {output_lpf_file} not found")

            self.index += 1


        elif (self.model == "ai_clone"):
            print("Synthesizing speech with CorentinJ")
            synthesize_speech(self.voice, content)
            end_time = time.time()

        elif (self.model == "commercial"):
            print("Synthesizing speech with ElevenLabs")
            eleven_tts(self.voice, content)
            end_time = time.time()


        synthesis_time = end_time - start_time
        print(f"Speech synthesis took {synthesis_time:.2f} seconds.")

        

        
    def play_effect(self, content):

        pygame.init()
        pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

        # Construct the file path based on the content parameter
        audio_file = f"tts_main\sounds\effects\{content}.wav"

        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except FileNotFoundError:
            print(f"Audio file {audio_file} not found")

            
    
    def speak_phrase(self, content):

        pygame.init()
        pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

        # Construct the file path based on the content parameter
        audio_file = f"tts_main\sounds\phrases\{self.voice}-{content}.wav"


        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except FileNotFoundError:
            print(f"Audio file {audio_file} not found")

            


    def play_music(self, content):
        
        pygame.init()
        pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

        # Construct the file path based on the content parameter
        audio_file = f"tts_main\sounds\music\{content}.mp3"

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

        
