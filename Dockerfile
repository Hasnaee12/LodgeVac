FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
# Installer MySQL client
RUN apt-get update && apt-get install -y default-libmysqlclient-dev
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
