import os

from flask import Flask, request, send_file, session, jsonify
import threading
import logging
from TTS.api import TTS
import random
import string
import json
import shutil


if os.path.exists("/home/appuser") == True:
    python_executable_path = "/usr/local/bin/python"
    generate_audio_path = "/home/appuser/generate_audio.py"
    speaker_base_dir = "/home/appuser/voices/"
    CUSTOM_VOICE_NAME = "michael"
    pp_dir_global = "/home/appuser/process_dir/"
    filter_path = "/home/appuser/arnndn/rnnoise-models/somnolent-hogwash-2018-09-01/sh.rnnn"
else:
    python_executable_path = "/coquio_ttsx_vish_coqui/cleancoquio_xtts_venv/bin/python"
    generate_audio_path = "/coquio_ttsx_vish_coqui/code/generate_audio.py"
    speaker_base_dir = "/coquio_ttsx_vish_coqui/api/code/voices/"
    CUSTOM_VOICE_NAME = "michael"
    pp_dir_global = "/coquio_ttsx_vish_coqui/api/code/process_dir/"
    filter_path = "/coquio_ttsx_vish_coqui/code/arnndn/rnnoise-models/somnolent-hogwash-2018-09-01/sh.rnnn"
def get_file_paths(directory_path):
    try:
        file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]
        return file_paths
    except OSError as e:
        print(f"Error: {e}")
        return []


def delete_audios(dizin):
    shutil.rmtree(dizin, ignore_errors=False, onerror=None)

def get_random_name():
   tmp = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(80))
   return str(tmp) 
    
def initialize_tts():
    try:
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        tts.to("cuda")
        return tts
    except Exception as e:
        print(e)
tts = initialize_tts()
app = Flask(__name__)

logging.basicConfig(filename='app.log', level=logging.INFO)
@app.route('/health')
def health():
    app.logger.info('HEALTH')
    
    return f"ALIVE"

@app.route('/')
def index():
    app.logger.info('ROOT')
    
    return f"ALIVE"
lock = threading.Lock()


@app.route('/process', methods=['POST'])
def process_text():
    if lock.acquire(blocking=False):
        try:
            try:
                data = request.get_json() 
                text = data.get('text', 'No text found')
                speaker = data.get('speaker', 'michael')
                speaker_wav_paths = get_file_paths(speaker_base_dir + speaker)
                sira = "001"
                app.logger.info('PROCESS')
                work_dir = get_random_name()
                pp_dir = pp_dir_global
                file_path= f'{pp_dir}{work_dir}/{CUSTOM_VOICE_NAME}_{sira}.wav'
                if not os.path.exists(pp_dir+"/"+work_dir):
                    os.makedirs(pp_dir+"/"+work_dir)    
                tts.tts_to_file(text=text, file_path=file_path, speaker_wav=speaker_wav_paths, language="en")
                return send_file(file_path, as_attachment=True)
            except Exception as e:
                    return jsonify({'error': str(e)}), 400
        except Exception as e:
            
            print(e)
            return 500
        finally:
            try:
                tmp = file_path.split("/")
                delete_path= '/'.join(tmp[:-1])
                delete_audios(delete_path)
            except Exception as e:
                print("delete tmp file error:" + str(e))
            lock.release()
    else:
        return "Another request is being processed. Please try again later." , 429


if __name__ == '__main__':
    app.run(debug=True, host ='0.0.0.0', port=5000,use_reloader=False)