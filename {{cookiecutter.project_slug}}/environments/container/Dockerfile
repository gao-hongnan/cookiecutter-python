ARG BUILDER_IMAGE=astral/uv:bookworm
ARG RUNNER_IMAGE=debian:bookworm-slim

# hadolint ignore=DL3006
FROM ${BUILDER_IMAGE} AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

WORKDIR /app
COPY .python-version .
RUN uv python install

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# hadolint ignore=DL3006
FROM ${RUNNER_IMAGE} AS runner

LABEL org.opencontainers.image.title="{{ cookiecutter.project_slug }}"
LABEL org.opencontainers.image.source="https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}"

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /python /python
COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot

WORKDIR /app

EXPOSE {{ cookiecutter.server_port }}
{% if cookiecutter.use_fastapi %}

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:{{ cookiecutter.server_port }}/')"]

CMD ["uvicorn", "{{ cookiecutter.package_name }}.main:app", "--host", "0.0.0.0", "--port", "{{ cookiecutter.server_port }}"]
{% else %}
CMD ["python", "-m", "{{ cookiecutter.package_name }}"]
{% endif %}
