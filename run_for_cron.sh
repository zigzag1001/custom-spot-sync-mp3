#!/bin/bash
cd /home/mele/mele_config/containers/custom-spot-sync-mp3
sudo docker compose up --no-recreate
curl -H "t: Spotify Synced" -d "Navidrome Synced" ntfy.sh/fail2ban_zmc_weekoldroadkill
