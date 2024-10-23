#!/usr/bin/env bash

# # clean codedeploy-agent files for a fresh install
# sudo rm -rf /home/ubuntu/install

# # install CodeDeploy agent
# sudo apt update
# sudo apt install ruby
# sudo apt install wget

# cd /home/ubuntu
# wget https://aws-codedeploy-us-east-1.s3.amazonaws.com/latest/install
# sudo chmod +x ./install 
# sudo ./install auto

# # delete app
# sudo rm -rf /home/ubuntu/jobfinderapi/*


#!/bin/bash

# Define log file
LOGFILE="/home/ubuntu/codedeploy_install.log"

# Function to log the output and errors
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOGFILE
}

# Clean CodeDeploy-agent files for a fresh install
log "Cleaning CodeDeploy-agent files..."
sudo rm -rf /home/ubuntu/install 2>>$LOGFILE
log "CodeDeploy-agent files cleaned."

# Update packages and install dependencies
log "Updating package list..."
sudo apt update >>$LOGFILE 2>&1
log "Package list updated."

log "Installing Ruby..."
sudo apt install -y ruby >>$LOGFILE 2>&1
log "Ruby installed."

log "Installing wget..."
sudo apt install -y wget >>$LOGFILE 2>&1
log "wget installed."

# Download and install CodeDeploy agent
log "Downloading CodeDeploy agent install script..."
cd /home/ubuntu
wget https://aws-codedeploy-us-east-1.s3.amazonaws.com/latest/install -O install >>$LOGFILE 2>&1
log "CodeDeploy agent install script downloaded."

log "Making install script executable..."
sudo chmod +x ./install 2>>$LOGFILE
log "Install script is now executable."

log "Running CodeDeploy agent install script..."
sudo ./install auto >>$LOGFILE 2>&1
log "CodeDeploy agent installed."

# Delete old application files
log "Deleting old application files in /home/ubuntu/jobfinderapi/..."
sudo rm -rf /home/ubuntu/jobfinderapi/* 2>>$LOGFILE
log "Old application files deleted."

log "CodeDeploy setup and cleaning completed."
