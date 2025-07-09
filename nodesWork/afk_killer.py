
#!/usr/bin/env python3
import subprocess
import time
from datetime import datetime, timedelta

# === КОНФИГ ===
AFK_TIMEOUT_MINUTES = 30        # Порог простоя в минутах
CHECK_INTERVAL_SECONDS = 60     # Как часто проверять (секунды)

def get_running_lab_containers():
    """
    Возвращает список имён запущенных контейнеров.
    Отфильтровываем по наличию '-' в имени (user-lab).
    """
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    names = result.stdout.strip().splitlines()
    # Оставляем только те, которые с дефисом (user-lab)
    return [n for n in names if "-" in n]

def get_container_start_time(name: str) -> datetime | None:
    """
    Через docker inspect получаем время старта контейнера.
    Возвращаем None, если не удалось распарсить.
    """
    result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.StartedAt}}", name],
        capture_output=True, text=True
    )
    iso_ts = result.stdout.strip()
    try:
        # Преобразуем Z в +00:00 для fromisoformat
        return datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    except Exception as e:
        print(f"[!] Не смогли получить время старта для {name}: {e}")
        return None

def has_recent_logs(name: str, since_minutes: int) -> bool:
    """
    Проверяем, есть ли логи контейнера за последние since_minutes минут.
    Если docker logs --since выдаёт хоть что-то — считаем, что контейнер активен.
    """
    # Формат '30m' поддерживается Docker CLI
    since_arg = f"{since_minutes}m"
    result = subprocess.run(
        ["docker", "logs", "--since", since_arg, name],
        capture_output=True, text=True
    )
    return bool(result.stdout.strip())

def stop_and_remove(name: str):
    """
    Останавливает и удаляет контейнер, если он ещё существует.
    """
    # Сначала пробуем остановить (если уже остановлен — пропустит)
    subprocess.run(["docker", "stop", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Затем удаляем
    subprocess.run(["docker", "rm", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"🗑 Контейнер {name} удалён как AFK")


from icecream import ic

def afk_cleaner_loop():
    """
    Основной цикл: каждые CHECK_INTERVAL_SECONDS секунд
    смотрим, какие контейнеры запущены дольше AFK_TIMEOUT_MINUTES
    и не пишут логи — и удаляем их.
    """
    while True:
        now = datetime.utcnow()
        timeout_delta = timedelta(minutes=AFK_TIMEOUT_MINUTES)
        running = get_running_lab_containers()
        ic(running)
        killed = 0

        for name in running:
            start_time = get_container_start_time(name)
            if not start_time:
                continue
            # Если контейнер запущен меньше порога — пропускаем
            if now - start_time < timeout_delta:
                continue
            # Если есть логи за последние AFK_TIMEOUT_MINUTES — активный
            if has_recent_logs(name, AFK_TIMEOUT_MINUTES):
                continue
            # Иначе — считаем AFK и удаляем
            stop_and_remove(name)
            killed += 1

        print(f"✅ Проверено {len(running)} контейнеров, удалено {killed} AFK.")
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    afk_cleaner_loop()

