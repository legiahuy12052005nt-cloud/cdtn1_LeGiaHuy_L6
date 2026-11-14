
FROM python:3.10.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Sao chép chương trình ETL và mã nguồn xử lý dữ liệu.
COPY run_etl.py .
COPY src/ ./src/

# Sao chép bộ kiểm thử để có thể chạy pytest trong Docker.
COPY tests/ ./tests/

COPY data/sample/ ./data/sample/

RUN mkdir -p data/raw data/processed data/rejected data/warehouse

RUN cp data/sample/orders_2024_2026.csv data/raw/ \
    && cp data/sample/order_items.csv data/raw/ \
    && cp data/sample/products.csv data/raw/ \
    && cp data/sample/stores.csv data/raw/

CMD ["python", "run_etl.py"]
