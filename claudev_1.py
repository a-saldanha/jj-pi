#basic_UI
#!/usr/bin/python3

import io
import json
import logging
import socketserver
from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

PAGE = """\
<html>
<head>
    <title>Dual Camera Control Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .camera-container {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }
        .camera-feed {
            text-align: center;
            flex: 1;
            margin: 0 10px;
        }
        .controls-container {
            display: flex;
            justify-content: space-between;
        }
        .control-panel {
            flex: 1;
            margin: 0 10px;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        .control-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="range"] {
            width: 100%;
        }
        .value-display {
            font-size: 0.9em;
            color: #666;
        }
        select {
            width: 100%;
            padding: 5px;
        }
        .toggle-switch {
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>Dual Camera Control Panel</h1>
    
    <div class="camera-container">
        <div class="camera-feed">
            <h2>Camera 1</h2>
            <img src="stream1.mjpg" width="640" height="480" />
        </div>
        <div class="camera-feed">
            <h2>Camera 2</h2>
            <img src="stream2.mjpg" width="640" height="480" />
        </div>
    </div>

    <div class="controls-container">
        <div class="control-panel">
            <h3>Camera 1 Controls</h3>
            <div class="control-group">
                <label>Brightness</label>
                <input type="range" min="-100" max="100" value="0" 
                    onchange="updateCamera(1, 'Brightness', this.value/100)">
                <span class="value-display">0</span>
            </div>
            
            <div class="control-group">
                <label>Contrast</label>
                <input type="range" min="0" max="3200" value="100"
                    onchange="updateCamera(1, 'Contrast', this.value/100)">
                <span class="value-display">1.0</span>
            </div>

            <div class="control-group">
                <label>Saturation</label>
                <input type="range" min="0" max="3200" value="100"
                    onchange="updateCamera(1, 'Saturation', this.value/100)">
                <span class="value-display">1.0</span>
            </div>

            <div class="control-group">
                <label>Sharpness</label>
                <input type="range" min="0" max="1600" value="100"
                    onchange="updateCamera(1, 'Sharpness', this.value/100)">
                <span class="value-display">1.0</span>
            </div>

            <div class="control-group">
                <label>AE Mode</label>
                <select onchange="updateCamera(1, 'AeExposureMode', parseInt(this.value))">
                    <option value="0">Normal</option>
                    <option value="1">Short</option>
                    <option value="2">Long</option>
                    <option value="3">Custom</option>
                </select>
            </div>

            <div class="toggle-switch">
                <label>
                    <input type="checkbox" checked
                        onchange="updateCamera(1, 'AeEnable', this.checked)">
                    Auto Exposure
                </label>
            </div>

            <div class="toggle-switch">
                <label>
                    <input type="checkbox" checked
                        onchange="updateCamera(1, 'AwbEnable', this.checked)">
                    Auto White Balance
                </label>
            </div>
        </div>

        <div class="control-panel">
            <h3>Camera 2 Controls</h3>
            <div class="control-group">
                <label>Brightness</label>
                <input type="range" min="-100" max="100" value="0"
                    onchange="updateCamera(2, 'Brightness', this.value/100)">
                <span class="value-display">0</span>
            </div>
            
            <div class="control-group">
                <label>Contrast</label>
                <input type="range" min="0" max="3200" value="100"
                    onchange="updateCamera(2, 'Contrast', this.value/100)">
                <span class="value-display">1.0</span>
            </div>

            <div class="control-group">
                <label>Saturation</label>
                <input type="range" min="0" max="3200" value="100"
                    onchange="updateCamera(2, 'Saturation', this.value/100)">
                <span class="value-display">1.0</span>
            </div>

            <div class="control-group">
                <label>Sharpness</label>
                <input type="range" min="0" max="1600" value="100"
                    onchange="updateCamera(2, 'Sharpness', this.value/100)">
                <span class="value-display">1.0</span>
            </div>

            <div class="control-group">
                <label>AE Mode</label>
                <select onchange="updateCamera(2, 'AeExposureMode', parseInt(this.value))">
                    <option value="0">Normal</option>
                    <option value="1">Short</option>
                    <option value="2">Long</option>
                    <option value="3">Custom</option>
                </select>
            </div>

            <div class="toggle-switch">
                <label>
                    <input type="checkbox" checked
                        onchange="updateCamera(2, 'AeEnable', this.checked)">
                    Auto Exposure
                </label>
            </div>

            <div class="toggle-switch">
                <label>
                    <input type="checkbox" checked
                        onchange="updateCamera(2, 'AwbEnable', this.checked)">
                    Auto White Balance
                </label>
            </div>
        </div>
    </div>

    <script>
        // Update value displays for range inputs
        document.querySelectorAll('input[type="range"]').forEach(input => {
            input.addEventListener('input', function() {
                this.nextElementSibling.textContent = 
                    (this.getAttribute('class') === 'brightness') ? 
                    this.value/100 : this.value/100;
            });
        });

        function updateCamera(cameraId, setting, value) {
            fetch('/update_camera', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    camera_id: cameraId,
                    setting: setting,
                    value: value
                })
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    console.error('Failed to update camera setting:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    </script>
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path in ['/stream1.mjpg', '/stream2.mjpg']:
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    current_output = output1 if self.path == '/stream1.mjpg' else output2
                    with current_output.condition:
                        current_output.condition.wait()
                        frame = current_output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/update_camera':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            camera = picam1 if data['camera_id'] == 1 else picam2
            try:
                # Update camera setting
                if data['setting'] in ['AeEnable', 'AwbEnable']:
                    camera.set_controls({data['setting']: data['value']})
                else:
                    camera.set_controls({data['setting']: float(data['value'])})
                
                response = {'success': True}
            except Exception as e:
                response = {'success': False, 'error': str(e)}
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Initialize cameras
picam1 = Picamera2(0)
picam2 = Picamera2(1)

# Configure cameras
picam1.configure(picam1.create_video_configuration(main={"size": (640, 480)}))
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))

# Create outputs
output1 = StreamingOutput()
output2 = StreamingOutput()

# Start recording
picam1.start_recording(JpegEncoder(), FileOutput(output1))
picam2.start_recording(JpegEncoder(), FileOutput(output2))

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    picam1.stop_recording()
    picam2.stop_recording()