from flask import Flask, jsonify, request
import threading
import logging
from werkzeug.serving import make_server

try:
    from sms import send_sms_message
except ImportError:
    def send_sms_message(p, m): return False, "Not running on Android"

try:
    from flashlight import toggle_android_flashlight
except ImportError:
    def toggle_android_flashlight(s): return False, "Not running on Android"

app = Flask(__name__)

# In-memory list to track API logs so Kivy can display them
api_logs = []

def log_request(msg):
    api_logs.append(msg)
    # Keep only the last 50 logs to prevent memory bloat
    if len(api_logs) > 50:
        api_logs.pop(0)
    print(f"[SERVER] {msg}")

@app.route('/')
def index():
    log_request("GET / - Status check")
    return jsonify({"status": "Gateway Server is Running", "version": "1.0"})

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    log_request("GET /api/test - Success")
    return jsonify({"message": "Server is reachable!"})

@app.route('/api/sms', methods=['POST'])
def handle_sms():
    data = request.get_json() or {}
    number = data.get('number')
    message = data.get('message')
    
    if not number or not message:
        log_request("POST /api/sms - Failed (Missing data)")
        return jsonify({"error": "Missing 'number' or 'message'"}), 400
        
    log_request(f"Sending OTP/Msg : {number}\nOTP: {message}")
    success, msg = send_sms_message(number, message)
    
    if success:
        return jsonify({"status": "success", "message": msg})
    else:
        log_request(f"SMS Error: {msg}")
        return jsonify({"status": "error", "message": msg}), 500

@app.route('/api/flashlight', methods=['POST'])
def handle_flashlight():
    data = request.get_json() or {}
    state = data.get('state')
    
    if state is None:
        log_request("POST /api/flashlight - Failed (Missing state)")
        return jsonify({"error": "Missing boolean 'state' (true/false)"}), 400
        
    log_request(f"POST /api/flashlight - State: {'ON' if state else 'OFF'}")
    success, msg = toggle_android_flashlight(state)
    
    if success:
        return jsonify({"status": "success", "message": msg})
    else:
        log_request(f"Flashlight Error: {msg}")
        return jsonify({"status": "error", "message": msg}), 500

flask_server = None
server_thread = None

class ServerThread(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.server = make_server('0.0.0.0', port, app)
        self.daemon = True

    def run(self):
        log_request("Server started...")
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        log_request("Server stopped.")

def start_flask_thread(port=5000):
    global server_thread
    if server_thread is None or not server_thread.is_alive():
        # Suppress verbose default flask logging to stdout
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        server_thread = ServerThread(port)
        server_thread.start()
        print(f"Flask server requested to start on port {port}")
        return True
    return False

def stop_flask_server():
    global server_thread
    if server_thread is not None and server_thread.is_alive():
        server_thread.shutdown()
        server_thread.join()
        server_thread = None
        return True
    return False