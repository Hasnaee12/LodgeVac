FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY . .
# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
# Installer MySQL client
RUN apt-get update && apt-get install -y default-libmysqlclient-dev
EXPOSE 5000
# Définir les variables d'environnement pour MySQL
ENV MYSQL_HOST=localhost
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=
ENV MYSQL_DB=mydb
# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]
