


FROM python:3.11-slim

WORKDIR /app

COPY app /app/app
COPY db_init.py /app/db_init.py
COPY requirements.txt /app/requirements.txt
COPY run.py /app/run.py

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

EXPOSE 8000
EXPOSE 80
# Можно создать БД при билде, но обычно лучше при старте (run.py сам это делает если надо)

CMD ["python", "run.py"]

