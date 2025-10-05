#!/bin/bash

sudo systemctl stop propbox.service
sudo systemctl disable propbox.service

sudo rm /etc/systemd/system/propbox.service

sudo systemctl daemon-reload

echo "PropBox uninstalled"
