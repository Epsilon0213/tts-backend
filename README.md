### This is the backend for the Virtual Classroom TTS App. 

## Main Code
All key logic and processing is stored inside /tts_main directory. The key folders for deployment should be in api.py, root.py, and chat_commands.py. TThe entry point of the backend is the root.py file.

Through the frontend, users can choose 4 different type of TTS model to use:
1. Robotic (Python pyttsx3 library)
2. Simple Cloning (Python pyttsx3 library + simple audio processing)
3. AI Cloning (this AI model is from CorentinJ and is stored locally in the /corentinj directory)
4. Commercial Cloning (calls API from ElevenLabs)

## IMPORTANT
Please download the three models here for the AI Cloning to work. Ensure that the models are stored in /corentinj_tts/saved_models/default/ directory.
https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Pretrained-models
