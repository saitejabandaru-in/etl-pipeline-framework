FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "-m", "etl.run", "--config", "pipeline_config.yaml", "--schedule", "manual"]
