FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sqlite_explorer.py .
COPY financial_data.db .

CMD ["python", "sqlite_explorer.py"]
