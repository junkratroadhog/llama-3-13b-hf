This repo contianer all the required files to setup you own LLaMA 3.13B model on your

Specs:
CPU = i7-8750H 
GPU = GTX 1070 
RAM = 16 GB
OS = Ubuntu 22.04.5 LTS (Jammy Jellyfish)

####################
### MANUAL STEPS ###
####################

1. Install GPU drivers
======================
sudo apt update
sudo apt install -y nvidia-driver-550
sudo reboot


2. install nvidia toolkit use below commands:
=============================================
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
