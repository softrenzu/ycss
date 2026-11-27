# YSCC VPS blog
From the repository root: cd docker. Copy env.example to .env, set SITE_URL, APPROVED_FOLDER_ID (a Drive folder containing only photos approved for public use and AI processing), OPENAI_API_KEY. Put the read-only service account JSON in secrets/google.json. Never commit credentials. Run mkdir -p runtime; docker compose run --rm --build blog; docker compose up -d web. The web service listens on localhost:8088; configure HTTPS reverse proxy separately.
Cron (JST host): 0 9 * * * cd /opt/ycss/docker && /usr/bin/docker compose run --rm blog >> /var/log/yscc-blog.log 2>&1
No unused approved photo or API failure: preserve existing publication and exit nonzero. Add new approved photos regularly. This implementation has not been tested against live credentials or a VPS.
