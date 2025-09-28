#!/bin/bash

sudo tee /etc/systemd/system/propbox.service > /dev/null << EOF
[Unit]
Description=PropBox
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/propbox/PropBox
Environment=PATH=/home/propbox/venv/bin
ExecStart=/home/propbox/venv/bin/python3 -u -m propbox
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable propbox.service
sudo systemctl start propbox.service

echo "PropBox installed"
