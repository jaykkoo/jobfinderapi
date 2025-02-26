#!/usr/bin/env bash

# # clean codedeploy-agent files for a fresh install
# sudo rm -rf /home/ubuntu/install

# # install CodeDeploy agent
# sudo apt update
# sudo apt install ruby-full
# sudo apt install wget

# cd /home/ubuntu
# wget https://aws-codedeploy-us-east-1.s3.amazonaws.com/latest/install
# sudo chmod +x ./install 
# sudo ./install auto

# # delete app@
# sudo rm -rf /home/ubuntu/jobfinderapi

#!/usr/bin/env bash

# Log file location
LOGFILE="/home/ubuntu/codedeploy_install.log"

# Function to log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOGFILE"
}

# Clean CodeDeploy agent files for a fresh install
log "Cleaning up previous installations..."
sudo rm -rf /home/ubuntu/install

# Update package list
log "Updating package list..."
if ! sudo apt update >> "$LOGFILE" 2>&1; then
    log "Failed to update package list."
    exit 1
fi

# Install Ruby and Wget
log "Installing Ruby and Wget..."
if ! sudo apt install -y ruby-full wget >> "$LOGFILE" 2>&1; then
    log "Failed to install Ruby or Wget."
    exit 1
fi

# Change to home directory
cd /home/ubuntu || { log "Failed to change directory to /home/ubuntu"; exit 1; }

# Download the CodeDeploy agent install script
log "Downloading CodeDeploy agent install script..."
if ! sudo wget https://aws-codedeploy-eu-west-3.s3.amazonaws.com/latest/install >> "$LOGFILE" 2>&1; then
    log "Failed to download the install script."
    exit 1
fi

# Make the script executable
log "Making install script executable..."
sudo chmod +x ./install 

# Install the CodeDeploy agent
log "Installing CodeDeploy agent..."
if ! sudo ./install auto >> "$LOGFILE" 2>&1; then
    log "Failed to install the CodeDeploy agent."
    exit 1
fi

# Cleanup
log "Cleaning up install files..."
sudo rm -rf /home/ubuntu/install

# Check if the CodeDeploy agent is running
if sudo service codedeploy-agent status >> "$LOGFILE" 2>&1; then
    log "CodeDeploy agent installed and is running."
else
    log "CodeDeploy agent installation failed or is not running."
fi
