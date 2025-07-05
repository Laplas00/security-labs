#!/bin/bash
# Запускаем Flask на фоне
python /app/run.py &
# Запускаем nginx (основным процессом)
nginx -g 'daemon off;' -c /etc/nginx/nginx.conf

