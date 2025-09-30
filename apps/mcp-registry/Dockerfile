FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY mcp_registry ./mcp_registry
EXPOSE 8080
CMD ["uvicorn", "mcp_registry.main:app", "--host", "0.0.0.0", "--port", "8080"]
