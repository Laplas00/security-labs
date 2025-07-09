
from datetime import datetime, timedelta
import subprocess
import re
import time

AFK_TIMEOUT_MINUTES = 30

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

def has_recent_logs(name, threshold_time):
    result = subprocess.run(
        ['docker', 'logs', name],
        capture_output=True, text=True
    )
    logs = result.stdout.strip().splitlines()
    for line in reversed(logs[-20:]):  # Проверяем последние 20 строк
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
    print(f"🗑 Killing AFK container: {name}")
    subprocess.run(['docker', 'rm', '-f', name], check=False)

def run_afk_cleanup():
    now = datetime.now()
    threshold = now - timedelta(minutes=AFK_TIMEOUT_MINUTES)
    containers = get_lab_containers()

    killed = 0
    for name in containers:
        start_time = get_container_started_at(name)
        if not start_time:
            continue
        if start_time > threshold:
            continue
        if has_recent_logs(name, threshold):
            continue
        stop_container(name)
        killed += 1

    print(f"✅ Checked {len(containers)} containers, killed {killed} AFK.")

if __name__ == "__main__":
    while True:
        print('Check afk containers if exists')
        run_afk_cleanup()
        time.sleep(60)
   
