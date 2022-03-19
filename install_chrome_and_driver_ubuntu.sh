#!/bin/bash

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt update
sudo apt -f install -y

CHROME_MAJOR_VER=$(google-chrome --version | sed --regex 's/Google Chrome ([0-9]+)\..*/\1/g')

echo Chrome Version: $CHROME_MAJOR_VER

DRIVER_VER=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VER})
echo Chrome Driver Version: $DRIVER_VER
curl -o chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/${DRIVER_VER}/chromedriver_linux64.zip

unzip chromedriver_linux64.zip
