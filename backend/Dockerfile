FROM python:3.11-slim

# Instalacja systemowego FFmpeg wewnątrz kontenera
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę kodu
COPY . .

# Wystawiamy port dla serwera deweloperskiego
EXPOSE 8000

# Odpalamy uvicorna, nasłuchując na wszystkich interfejsach (0.0.0.0)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]