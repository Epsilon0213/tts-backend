import sys
from sound_engine import soundEngine
from pygame import mixer, _sdl2

# class CircularArray:
#     def __init__(self, size):
#         self.size = size
#         self.array = [None] * size
#         self.insert_pointer = 0
#         self.process_pointer = 0

#     def add_string(self, text):
#         self.array[self.insert_pointer] = text
#         self.insert_pointer = (self.insert_pointer + 1) % self.size


class commandBot:

    def __init__(self):
        self.commands = {
        "talk": self.bot_talk,
        "speak_phrase": self.bot_speak_phrase,
        "music_on": self.bot_play_music,
        "music_off": self.bot_stop_music,
        "voice_select": self.bot_voice_select,
        "model_select": self.bot_model_select,
        "sound_effect": self.bot_play_effect,
        "ques": self.bot_question,
        }
        # The pyTTSEngine will be instantiated  when the meetsCommandBot is intantiated.
        self.sound_engine = soundEngine()
        
    def extract_command(self, text):
        if text.startswith("/"):
            command_end_index = text.find(' ')
            command = text[1:command_end_index]

            return command, text[command_end_index + 1:]
        else:
            return None, None


    def process_command(self, text):
        # Check if end command is called
        # if text == "/end":
        #     self.end()

        # Else proceed with command handling
        command, content = self.extract_command(text)

        if command is None:
            return
        else:
            command_match = self.commands.get(command, None) # If command is detected (based on first char /), map it against dictionary to find execute corresponding function

            # If command_handler unable to obtain successful match, command_handler returns None
            if command_match is None:
                print("User called command but command unknown")
            elif content:
                return command_match(content) # If successful match, pass the text part (only if it is not empty) after the command into the function
                # Returns data for question function and return back to TTS Chat App

    def bot_voice_select(self,content):
        self.sound_engine.voice_select(content)

    def bot_model_select(self, content):
        self.sound_engine.model_select(content)


    def bot_talk(self, content):
        self.sound_engine.talk(content)

        # try:
        #     self.tts_engine.tts_pytts(content)
        # except:
        #     return
    
    def bot_play_effect(self, content):
        self.sound_engine.play_effect(content)


    def bot_speak_phrase(self, content):
        self.sound_engine.speak_phrase(content)

    def bot_play_music(self,content):
        self.sound_engine.play_music(content)

    def bot_stop_music(self,content):
        self.sound_engine.stop_music(content)

    def bot_question(self, content):
        return content
        


    def end(self):
        print("Terminating program now...")
        sys.exit(0)


    

# bot = meetsCommandBot()
# text = "/talk Hi, how is everyone doing"
# bot.process_command(text)

# text2 = "#tts Hi, this is a test"
# bot.process_command(text2)




# prev_chat_list = ["a", "b"]
# new_chat_list = ["b"]

# ca = CircularArray(3)

# print("Before add string. Insert pointer position now in:", ca.insert_pointer)
# ca.add_string(str(set(prev_chat_list) ^ set(new_chat_list))) # Uses set to find non-overlaps and then appends it to circular array
# print("After add string. Insert pointer position now in:", ca.insert_pointer)

# print(ca.array)


# chat_messages_buffer = CircularArray(10)
# buffer_pointer = chat_messages_buffer.pointer
# chat_messages_buffer.add_string("test test")


# print("Pointer position now in:", buffer_pointer)
# bot.process_command(chat_messages_buffer.array[buffer_pointer])
# buffer_pointer += 1
# print("Pointer position now in:", buffer_pointer)