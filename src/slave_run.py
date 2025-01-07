#slave_run
from slave_node import SlaveNode
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python slave_run.py <slave_id>")
        sys.exit(1)
        
    slave_id = sys.argv[1]
    slave = SlaveNode(slave_id)
    slave.connect_to_master()
    
if __name__ == "__main__":
    main()