# Użyj oficjalnego obrazu Python jako bazy
FROM python:3.9

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki projektu do kontenera
COPY . .

# Zainstaluj wymagane pakiety
RUN pip install --no-cache-dir -r requirements.txt

# Komenda do uruchomienia serwera
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
