from datetime import datetime, timedelta
import subprocess
import re
from pathlib import Path

# === CONFIG ===
ACCESS_LOG_PATH = "/root/security-labs/nodesWork/traefik_logs"  # измени при необходимости
AFK_TIMEOUT_MINUTES = 30

# === REGEX: log format ===
log_pattern = re.compile(r'\[(.*?)\].*?"\S+@\w+"\s".*?"\s".*?"\s\d+\s"(.*?)@"')

# === TIME PARSING ===
def parse_log_timestamp(raw_ts):
    try:
        return datetime.strptime(raw_ts, "%d/%b/%Y:%H:%M:%S %z")
    except ValueError:
        return None

# === Чтение access.log
def get_last_seen_containers():
    last_seen = {}
    try:
        lines = Path(ACCESS_LOG_PATH).read_text().splitlines()
    except FileNotFoundError:
        print("❌ Log file not found")
        return last_seen

    for line in lines:
        match = re.search(r'\[(.*?)\].*?"(\S+)@\w+"', line)
        if match:
            ts_raw, container = match.groups()
            ts = parse_log_timestamp(ts_raw)
            if ts:
                last_seen[container] = ts
    return last_seen

# === AFK фильтр
def get_afk_containers(last_seen):
    now = datetime.now(tz=next(iter(last_seen.values())).tzinfo)
    threshold = now - timedelta(minutes=AFK_TIMEOUT_MINUTES)
    ic(threshold)
    return [name for name, ts in last_seen.items() if ts < threshold]

# === Удаление контейнера
def stop_container(container):
    print(f"🗑 Killing AFK container: {container}")
    subprocess.run(["docker", "rm", "-f", container])

# === MAIN
if __name__ == "__main__":
    last_seen = get_last_seen_containers()
    afk = get_afk_containers(last_seen)

    for container in afk:
        stop_container(container)

    print(f"✅ Checked {len(last_seen)} containers. Killed {len(afk)}.")

