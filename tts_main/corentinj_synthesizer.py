import sys
import os
import numpy as np
from pathlib import Path
import soundfile as sf
from playsound import playsound
import glob
import pygame
import time

sys.path.insert(1, 'corentinj_tts')

from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder


# Initialises encoder, synthesizer and vocoder model when root is run
encoder.load_model(Path("corentinj_tts/saved_models/default/encoder.pt"))
synthesizer = Synthesizer(Path("corentinj_tts/saved_models/default/synthesizer.pt"))
vocoder.load_model(Path("corentinj_tts/saved_models/default/vocoder.pt"))

# Computes embedding from input audio and stores it in global variable <embedding>
def _compute_embedding(audio):
  global embedding 
  embedding = None
  SAMPLE_RATE = 22050 # Set sample rate
  embedding = encoder.embed_utterance(encoder.preprocess_wav(audio, SAMPLE_RATE))

# Synthesizes audio with input text and embedding variable and returns a audio waveform
def synthesize_with_embed(embed, text):
  specs = synthesizer.synthesize_spectrograms([text], [embed])
  generated_wav = vocoder.infer_waveform(specs[0])
  generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
  return generated_wav

def corentinj_tts(speaker_voice, text, output_file):
    
    speaker_voice_file = f"{speaker_voice}-train-speech.wav"
    print("Extracting embedding from", speaker_voice_file)
    
    _compute_embedding("corentinj_tts/speaker_voices/" + speaker_voice_file)
    output_audio = synthesize_with_embed(embedding, text)


    # Set the new filename
    out_file = sf.write(output_file, output_audio, synthesizer.sample_rate)

    return out_file


    











