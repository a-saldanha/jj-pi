#initial_pi_setup
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git python3-pip ntp libcamera-dev python3-picamera2

# Enable camera interface
sudo raspi-config
# Navigate to Interface Options -> Camera -> Enable

# Set static IP addresses in /etc/dhcpcd.conf
sudo nano /etc/dhcpcd.conf

# Add for master:
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1

# Add for slave1:
interface eth0
static ip_address=192.168.1.101/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1

# Add for slave2:
interface eth0
static ip_address=192.168.1.102/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1