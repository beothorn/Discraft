#!/bin/bash
sudo apt-get update
sudo apt-get -y install python3-pip
pip3 install discord.py==0.16.12
pip3 install pexpect
sudo apt install openjdk-11-jre-headless
wget https://launcher.mojang.com/v1/objects/ed76d597a44c5266be2a7fcd77a8270f1f0bc118/server.jar
java -jar server.jar
sed -i "s/false/true/" eula.txt
