FROM python:3.11-slim

WORKDIR /app
COPY app /app/app
COPY db_init.py /app/db_init.py
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Инициализация базы при запуске (если надо)
CMD ["sh", "-c", "python /app/db_init.py && python -m app.utils.app"]

