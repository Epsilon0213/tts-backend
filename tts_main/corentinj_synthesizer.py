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
  syn_time = time.time()
  specs = synthesizer.synthesize_spectrograms([text], [embed])
  synth_time = time.time() - syn_time
  print(f"Synthesizer took {synth_time:.2f} seconds.")

  voc_time = time.time()
  generated_wav = vocoder.infer_waveform(specs[0])
  vocoder_time = time.time() - voc_time
  print(f"Vocoder took {vocoder_time:.2f} seconds.")

  generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
  return generated_wav

def synthesize_speech(speaker_voice, text):
    
    start_time = time.time()
  
    speaker_voice_file = f"{speaker_voice}-train-speech.wav"
    print("Extracting embedding from", speaker_voice_file)
    
    encode_time = time.time()
    _compute_embedding("corentinj_tts/speaker_voices/" + speaker_voice_file)
    encoder_time = time.time() - encode_time
    print(f"Encoder took {encoder_time:.2f} seconds.")


    output_audio = synthesize_with_embed(embedding, text)

    outdir = "corentinj_tts/tts_ai_history/"

    # Find existing files with the desired naming pattern
    existing_files = glob.glob(os.path.join(outdir, f"tts_{speaker_voice}_*.wav"))

    # Determine the next file number for the current speaker voice
    file_number = max([int(os.path.splitext(os.path.basename(f))[0].split("_")[2]) for f in existing_files], default=0) + 1

    # Set the new filename
    filename = f"tts_{speaker_voice}_{file_number}.wav"
    out_dest = os.path.join(outdir, filename)
    out_file = sf.write(out_dest, output_audio, synthesizer.sample_rate)

    pygame.init()
    pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

    # Construct the file path based on the content parameter
    out_file = f"corentinj_tts/tts_ai_history/{filename}"

    try:
        pygame.mixer.music.load(out_file)
        end_time = time.time()
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except FileNotFoundError:
        print(f"Audio file {out_file} not found")

    synthesis_time = end_time - start_time
    print(f"Speech synthesis took {synthesis_time:.2f} seconds.")

    










# SAMPLE_RATE = 22050 # Set sample rate
# # SAMPLE_RATE = 44100 # Set sample rate
# embedding = None # Initialise embedding variable
# speaker_voice = "On Rosie  Fat Ugly Face.wav"

# text = "You don't look very attractive do you? You shouldn't be here."

# _compute_embedding("corentinj_tts/speaker_voices/" + speaker_voice)
# output_audio = synthesize(embedding, text)

# # Define directory path for output
# outdir = "corentinj_tts/output_waveforms/"
# filename = "proper_test_40k.wav"
# out_dest = os.path.join(outdir, filename)
# sf.write(out_dest, output_audio, synthesizer.sample_rate)













