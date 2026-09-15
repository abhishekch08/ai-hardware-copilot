FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY config ./config
COPY agents ./agents
COPY governance ./governance
COPY schemas ./schemas
COPY conference ./conference
COPY web ./web
RUN python -m pip install --no-cache-dir .

RUN useradd --create-home --uid 10001 copilot \
    && mkdir -p /data /projects \
    && chown -R copilot:copilot /data /projects
USER copilot

EXPOSE 8080
VOLUME ["/data", "/projects"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2).read()"

ENTRYPOINT ["hardware-copilot", "serve", "--repo-root", "/app", "--data-root", "/data", "--projects-root", "/projects", "--host", "0.0.0.0", "--port", "8080"]
