FROM docker.arvancloud.ir/python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --index-url https://mirror2.chabokan.net/pypi/simple/ --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]