#slave_final
import socket
import json
import time
import os
from picamera2 import Picamera2
from config import Config

class SlaveNode:
    def __init__(self, slave_id):
        self.slave_id = slave_id
        self.cameras = []
        self.setup_directories()
        self.initialize_cameras()
        
    def setup_directories(self):
        os.makedirs(Config.VIDEO_PATH, exist_ok=True)
        
    def initialize_cameras(self):
        try:
            self.cameras = [
                Picamera2(0),
                Picamera2(1)
            ]
            
            # Configure both cameras
            for i, cam in enumerate(self.cameras):
                config = cam.create_video_configuration(
                    main={"size": (1920, 1080)},
                    lores={"size": (640, 480)},
                    display="lores"
                )
                cam.configure(config)
                print(f"Camera {i} initialized")
                
        except Exception as e:
            print(f"Camera initialization error: {e}")
            
    def connect_to_master(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((Config.MASTER_IP, Config.COMMAND_PORT))
            
            # Send handshake
            handshake = {
                'id': self.slave_id,
                'cameras': len(self.cameras)
            }
            self.socket.send(json.dumps(handshake).encode())
            print("Connected to master")
            
            self.handle_commands()
            
        except Exception as e:
            print(f"Connection error: {e}")
            
    def handle_commands(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                    
                cmd = json.loads(data.decode())
                if cmd['type'] == 'record':
                    self.record_video(cmd['start_time'], cmd['duration'])
                    
            except Exception as e:
                print(f"Command handling error: {e}")
                break
                
        self.socket.close()
        
    def record_video(self, start_time, duration):
        # Wait for synchronized start
        wait_time = start_time - time.time()
        if wait_time > 0:
            time.sleep(wait_time)
            
        timestamp = int(time.time())
        
        try:
            # Start recording on all cameras
            for i, cam in enumerate(self.cameras):
                filename = f"{Config.VIDEO_PATH}/cam_{self.slave_id}_{i}_{timestamp}.mp4"
                cam.start_recording(filename)
                print(f"Started recording camera {i}")
                
            # Record for specified duration
            time.sleep(duration)
            
            # Stop recording on all cameras
            for i, cam in enumerate(self.cameras):
                cam.stop_recording()
                print(f"Stopped recording camera {i}")
                
            # Send completion notification
            response = {
                'type': 'recording_complete',
                'timestamp': timestamp,
                'status': 'success'
            }
            self.socket.send(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Recording error: {e}")
            response = {
                'type': 'recording_complete',
                'timestamp': timestamp,
                'status': 'error',
                'error': str(e)
            }
            self.socket.send(json.dumps(response).encode())