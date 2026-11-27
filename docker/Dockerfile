FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 TZ=Asia/Tokyo
RUN apt-get update && apt-get install -y --no-install-recommends openssl ca-certificates tzdata && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY index.html app.js styles.css football.css favicon.svg robots.txt ./
COPY data ./data
COPY scripts ./scripts
COPY config ./config
ENTRYPOINT ["python", "scripts/vps_publish.py"]
