#master_run
from master_node import MasterNode

def main():
    master = MasterNode()
    master.start_server()
    
if __name__ == "__main__":
    main()
