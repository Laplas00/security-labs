FROM python:3.11-slim

WORKDIR /app

COPY app /app/app
COPY db_init.py /app/db_init.py
COPY requirements.txt /app/requirements.txt
COPY run.py /app/run.py

RUN apt update && apt install net-tools -y
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
EXPOSE 5000
# Можно создать БД при билде, но обычно лучше при старте (run.py сам это делает если надо)

CMD ["python", "run.py"]

