# On master Pi, in Python console:
from master_node import MasterNode
master = MasterNode()
master.start_server()
# Wait for slaves to connect
master.trigger_recording(duration=5)  # 5-second test recording