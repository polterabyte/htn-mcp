FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY mcp_http ./mcp_http
EXPOSE 7000
CMD ["uvicorn", "mcp_http.app:app", "--host", "0.0.0.0", "--port", "7000"]
