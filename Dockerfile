FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN dbt deps --project-dir transforms

EXPOSE 8501

CMD ["python", "pipeline/flow.py"]
