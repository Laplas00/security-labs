
# Stage 1 — Backend
FROM python:3.10-slim as backend

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Stage 2 — Nginx Proxy (Frontend)
FROM nginx:alpine as frontend

COPY nginx.conf /etc/nginx/nginx.conf

# Stage 3 — Final image
FROM python:3.10-slim

WORKDIR /app

# Копируем backend с зависимостями
COPY --from=backend /app /app
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Копируем nginx
RUN apt update && apt install -y nginx
COPY --from=frontend /etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Статика и шаблоны
RUN mkdir -p /app/templates
COPY /templates/index.html /app/templates/index.html

# 🧠 Запуск: nginx + gunicorn (многопроцессный сервер для Flask)
CMD service nginx start && gunicorn app:app --bind 0.0.0.0:5000 --workers 1 --threads 2 --timeout 90

EXPOSE 5000

