FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 TZ=Asia/Tokyo
WORKDIR /app
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY index.html app.js styles.css football.css favicon.svg robots.txt ./
COPY data ./data
COPY scripts/daily_blog.py ./scripts/daily_blog.py
COPY docker/publish.py ./publish.py
ENTRYPOINT ["python","/app/publish.py"]
