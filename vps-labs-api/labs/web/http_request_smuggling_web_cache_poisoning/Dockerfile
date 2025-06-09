
# Stage 1 — Backend
FROM python:3.10-slim as backend

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2 — Nginx Proxy (Frontend)
FROM nginx:alpine as frontend

# Заменим дефолтный конфиг
COPY nginx.conf /etc/nginx/nginx.conf

# Stage 3 — Финальный контейнер с nginx и backend
FROM python:3.10-slim

# Копируем backend
COPY --from=backend /app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Копируем nginx
RUN apt update && apt install -y nginx
COPY --from=frontend /etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Копируем index.html в нужное место (если нужно)
RUN mkdir -p /app/templates
COPY /templates/index.html /app/templates/index.html

# Настраиваем запуск: nginx + flask
CMD service nginx start && python app.py
EXPOSE 80

