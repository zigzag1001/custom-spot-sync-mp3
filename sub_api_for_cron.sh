#!/bin/bash
cd /home/debian/mele_config/containers/custom-spot-sync-mp3
sudo docker compose -f compose.sub_api.yml up --no-recreate
