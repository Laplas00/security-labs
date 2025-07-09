
from datetime import datetime, timedelta
import subprocess
import re
import time

AFK_TIMEOUT_MINUTES = 30
CHECK_INTERVAL_SECONDS = 60

def get_lab_containers():
    result = subprocess.run(
        ['docker', 'ps', '--format', '{{.Names}}'],
        capture_output=True, text=True
    )
    containers = result.stdout.strip().splitlines()
    return [name for name in containers if '-' in name]

def get_container_started_at(name):
    result = subprocess.run(
        ['docker', 'inspect', '-f', '{{.State.StartedAt}}', name],
        capture_output=True, text=True
    )
    try:
        return datetime.fromisoformat(result.stdout.strip().replace("Z", "+00:00"))
    except Exception as e:
        print(f"[!] Failed to parse start time for {name}: {e}")
        return None

def container_exists(name):
    result = subprocess.run(
        ['docker', 'inspect', name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def has_recent_logs(name, threshold_time):
    result = subprocess.run(
        ['docker', 'logs', name],
        capture_output=True, text=True
    )
    logs = result.stdout.strip().splitlines()
    for line in reversed(logs[-20:]):  # Последние 20 строк
        match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', line)
        if match:
            try:
                log_time = datetime.fromisoformat(match.group(1))
                if log_time > threshold_time:
                    return True
            except:
                continue
    return False

def stop_container(name):
    if not container_exists(name):
        print(f"⚠️  Container {name} already stopped or removed.")
        return
    print(f"🗑 Killing AFK container: {name}")
    subprocess.run(['docker', 'rm', '-f', name], check=False)

def run_afk_loop():
    while True:
        now = datetime.now()
        threshold = now - timedelta(minutes=AFK_TIMEOUT_MINUTES)
        containers = get_lab_containers()
        killed = 0

        for name in containers:
            start_time = get_container_started_at(name)
            if not start_time or start_time > threshold:
                continue
            if has_recent_logs(name, threshold):
                continue
            stop_container(name)
            killed += 1

        print(f"✅ Checked {len(containers)} containers. Killed {killed} AFK.")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_afk_loop()

