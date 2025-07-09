from datetime import datetime, timedelta
import subprocess
import re
from pathlib import Path

# === CONFIG ===
ACCESS_LOG_PATH = "/root/security-labs/nodesWork/traefik_logs/access.log"  # измени при необходимости
AFK_TIMEOUT_MINUTES = 1


def parse_log_timestamp(raw: str) -> datetime | None:
    try:
        # adjust this to match your actual log format
        # e.g. 2025-07-09T14:33:22+00:00 or whatever you log
        return datetime.fromisoformat(raw)
    except Exception as e:
        ic(f"Failed to parse timestamp {raw!r}: {e}")
        return None

def get_last_seen_containers() -> dict[str, datetime]:
    last_seen: dict[str, datetime] = {}
    try:
        lines = Path(ACCESS_LOG_PATH).read_text().splitlines()
    except FileNotFoundError:
        print("❌ Log file not found:", ACCESS_LOG_PATH)
        return last_seen

    for line in lines:
        # tweak this regex to match your actual log entries
        match = re.search(r'\[([^\]]+)\].*?"(\S+)@\w+"', line)
        if not match:
            continue

        ts_raw, container = match.groups()
        ts = parse_log_timestamp(ts_raw)
        if ts:
            last_seen[container] = ts

    return last_seen

def get_afk_containers(last_seen: dict[str, datetime]) -> list[str]:
    if not last_seen:
        print("ℹ️  No containers seen in logs; nothing to kill.")
        return []

    # pick any tzinfo from your timestamps
    tz = next(iter(last_seen.values())).tzinfo
    now = datetime.now(tz=tz)
    threshold = now - timedelta(minutes=AFK_TIMEOUT_MINUTES)
    ic("AFK threshold:", threshold.isoformat())

    return [name for name, ts in last_seen.items() if ts < threshold]

def stop_container(container: str):
    print(f"🗑 Killing AFK container: {container}")
    try:
        subprocess.run(
            ["docker", "rm", "-f", container],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"✅ Successfully killed {container}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to kill {container}: {e.stderr.strip()}")

if __name__ == "__main__":
    last_seen = get_last_seen_containers()
    afk = get_afk_containers(last_seen)

    for c in afk:
        stop_container(c)

    print(f"✅ Checked {len(last_seen)} containers; killed {len(afk)}.")
