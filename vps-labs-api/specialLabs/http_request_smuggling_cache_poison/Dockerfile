

FROM python:3.11

WORKDIR /app

COPY app /app/app
COPY db_init.py /app/db_init.py
COPY requirements.txt /app/requirements.txt
COPY run.py /app/run.py
COPY nginx.conf /etc/nginx/nginx.conf

RUN pip install --no-cache-dir -r requirements.txt


RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils dialog procps net-tools curl && \
    apt-get install -y --no-install-recommends nginx && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000
EXPOSE 5000

# Bash-скрипт для запуска двух процессов
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]

