#!/bin/bash
cd /home/mele/mele_config/containers/custom-spot-sync-mp3
sudo docker compose -f compose.sync.yml up --no-recreate
