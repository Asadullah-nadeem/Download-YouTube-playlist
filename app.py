from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
from downloader import download_media
from logger import CustomLogger

app = Flask(__name__)
socketio = SocketIO(app)

stop_flags = {}

def log_callback(message):
    socketio.emit('log', {'message': message})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    playlist_url = data['url']
    download_type = data['type']
    resolution = data.get('resolution', None)

    stop_flag = threading.Event()
    stop_flags[data['id']] = stop_flag

    def start_download():
        try:
            download_media(playlist_url, 'downloads', download_type, resolution, log_callback, stop_flag)
        except Exception as e:
            log_callback(f"Error: {e}")
        finally:
            socketio.emit('download_complete', {'id': data['id']})

    threading.Thread(target=start_download).start()
    return jsonify({'status': 'started'})

@app.route('/stop', methods=['POST'])
def stop_download():
    data = request.json
    download_id = data['id']
    if download_id in stop_flags:
        stop_flags[download_id].set()
        return jsonify({'status': 'stopping'})
    return jsonify({'status': 'not_found'}), 404

if __name__ == '__main__':
    socketio.run(app, debug=True)
