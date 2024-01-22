FROM python:3.11.5

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
COPY root.py /app/
COPY Web /app/Web/

# Installez les dépendances
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Exposez le port sur lequel votre application Flask s'exécutera
EXPOSE 5000

CMD ["pipenv", "run", "python", "root.py"]
