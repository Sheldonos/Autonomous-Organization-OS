FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN useradd -r -u 10001 faos && mkdir -p /var/lib/faos && chown -R faos:faos /var/lib/faos /app
USER faos
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 FAOS_CAPABILITY_DB=/var/lib/faos/capabilities.db
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=3).read()"
CMD ["python","scripts/control_api.py","--host","0.0.0.0","--port","8080"]
