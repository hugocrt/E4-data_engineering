# Utilisez une image de base avec Python
FROM python:3.11.5

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY Pipfile Pipfile.lock /app/
COPY Scraping /app/Scraping/

# Installez les dépendances
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Commande par défaut pour exécuter votre application Scrapy
CMD ["pipenv", "run", "scrapy", "crawl", "senscritique"]
