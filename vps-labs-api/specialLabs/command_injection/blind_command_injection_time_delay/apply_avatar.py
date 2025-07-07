#!/usr/bin/env python3
import sys, requests, io


print('apply avatar runned')
user_id   = sys.argv[1]
avatar_url= sys.argv[2]

# simulate downloading & processing the avatar
resp = requests.get(avatar_url, timeout=2)
resp.raise_for_status()
with open(f"/tmp/avatar_{user_id}.png", "wb") as f:
    f.write(resp.content)
print('apply avatar finished')
