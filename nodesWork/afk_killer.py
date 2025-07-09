from datetime import datetime, timedelta
import subprocess
import re
from pathlib import Path

# === CONFIG ===
ACCESS_LOG_PATH = "/root/security-labs/nodesWork/traefik_logs/access.log"  # измени при необходимости
AFK_TIMEOUT_MINUTES = 1



def parse_log_timestamp(raw):
    try:
        return datetime.fromisoformat(raw)
    except:
        return None

def get_last_seen_containers():
    last_seen = {}
    for line in Path(ACCESS_LOG_PATH).read_text().splitlines():
        m = re.search(r'\[([^\]]+)\].*?"(\S+)@\w+"', line)
        if not m: 
            continue
        ts_raw, name = m.groups()
        ts = parse_log_timestamp(ts_raw)
        if ts:
            last_seen[name] = ts
    return last_seen

def get_running_containers() -> set[str]:
    p = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        check=True,
        stdout=subprocess.PIPE,
        text=True
    )
    return set(filter(None, p.stdout.splitlines()))

def get_afk_containers(last_seen):
    if not last_seen:
        return []
    now       = datetime.now(tz=next(iter(last_seen.values())).tzinfo)
    threshold = now - timedelta(minutes=AFK_TIMEOUT_MINUTES)
    return [name for name, ts in last_seen.items() if ts < threshold]

def stop_container(name):
    print(f"🗑 Killing AFK container: {name}")
    subprocess.run(["docker", "rm", "-f", name], check=False)

if __name__ == "__main__":
    last_seen = get_last_seen_containers()
    running   = get_running_containers()

    # only handle containers that are both seen *and* still up
    candidates = {n:ts for n,ts in last_seen.items() if n in running}

    afk = get_afk_containers(candidates)
    for c in afk:
        stop_container(c)

    print(f"✅ Checked {len(candidates)} running containers; killed {len(afk)}.")
    
