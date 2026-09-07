FROM python:3.13-slim
WORKDIR /app
COPY control_plane/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY control_plane/agentic_sdlc_cp /app/agentic_sdlc_cp
ENV PYTHONPATH=/app
EXPOSE 8787
CMD ["python", "-m", "agentic_sdlc_cp.cli", "serve", "--host", "0.0.0.0", "--port", "8787"]
