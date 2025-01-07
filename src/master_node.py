#master_final
import socket
import threading
import time
import json
import os
from config import Config

class MasterNode:
    def __init__(self):
        self.slaves = {
            'slave1': {'ip': Config.SLAVE1_IP, 'status': 'disconnected'},
            'slave2': {'ip': Config.SLAVE2_IP, 'status': 'disconnected'}
        }
        self.setup_directories()
        
    def setup_directories(self):
        os.makedirs(Config.VIDEO_PATH, exist_ok=True)
        
    def start_server(self):
        # Command server
        self.cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cmd_socket.bind(('0.0.0.0', Config.COMMAND_PORT))
        self.cmd_socket.listen(5)
        print("Master node started, waiting for slaves...")
        
        # Start accepting connections
        self.accept_connections()
        
    def accept_connections(self):
        while True:
            conn, addr = self.cmd_socket.accept()
            threading.Thread(target=self.handle_slave, args=(conn, addr)).start()
            
    def handle_slave(self, conn, addr):
        try:
            data = conn.recv(1024)
            slave_info = json.loads(data.decode())
            slave_id = slave_info['id']
            
            self.slaves[slave_id]['status'] = 'connected'
            self.slaves[slave_id]['connection'] = conn
            print(f"Slave {slave_id} connected from {addr}")
            
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                    
                response = json.loads(data.decode())
                print(f"Received from {slave_id}: {response}")
                
        except Exception as e:
            print(f"Error handling slave {addr}: {e}")
        finally:
            conn.close()
            self.slaves[slave_id]['status'] = 'disconnected'
            
    def trigger_recording(self, duration):
        if not all(slave['status'] == 'connected' for slave in self.slaves.values()):
            print("Not all slaves are connected!")
            return
            
        start_time = time.time() + 1
        cmd = {
            'type': 'record',
            'start_time': start_time,
            'duration': duration
        }
        
        for slave_id, slave in self.slaves.items():
            try:
                slave['connection'].send(json.dumps(cmd).encode())
                print(f"Triggered recording on {slave_id}")
            except Exception as e:
                print(f"Error triggering {slave_id}: {e}")
