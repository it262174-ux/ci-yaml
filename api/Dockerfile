# ---------- Builder Stage ----------
FROM python:3.13-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /build

COPY requirements.txt .

RUN python -m venv $VIRTUAL_ENV \
    && pip install --no-cache-dir -r requirements.txt


# ---------- Runtime Stage ----------
FROM python:3.13-slim AS runtime

LABEL org.opencontainers.image.title="devops-shop-api" \
      org.opencontainers.image.version="1.0" \
      org.opencontainers.image.description="DevOps Shop API"

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY --from=builder /opt/venv /opt/venv

COPY --chown=appuser:appuser --chmod=644 app.py .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]