from flask import Flask, request, jsonify
from flask_cors import CORS
from chat_commands import commandBot


class APIServer:
    def __init__(self):
        self.app = Flask(__name__)
        # The meetsCommandBot will be instantiated when APIServer is instantiated
        self.bot = commandBot()
        self.app.add_url_rule('/submit-message', 'submit_message', self.handle_api, methods=['POST'])
        self.app.add_url_rule('/music-player', 'music_player', self.handle_api, methods=['POST'])
        self.app.add_url_rule('/voice-select', 'voice_select', self.handle_api, methods=['POST'])
        self.app.add_url_rule('/model-select', 'model_select', self.handle_api, methods=['POST'])


        # Enable CORS to support same origin programs
        CORS(self.app)

    def handle_api(self):
        data = request.get_json()
        message = data['message']
        print(message)
        response = self.bot.process_command(message)
        return jsonify({'response': response})
    

    def run(self):
        self.app.run(host='0.0.0.0', port=105)




