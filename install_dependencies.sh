#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip python-dev build-essential 
sudo pip3 install --upgrade pip 
sudo pip3 install --upgrade virtualenv 
sudo pip3 install requests
sudo pip3 install InstagramApi --ignore-installed