FROM node:20-alpine
WORKDIR /app

# Kopiujemy pliki z zależnościami i instalujemy je
COPY package*.json ./
RUN npm install

# Kopiujemy resztę kodu
COPY . .

EXPOSE 5173

# Uruchamiamy Vite, wymuszając nasłuchiwanie na wszystkich interfejsach
CMD ["npm", "run", "dev", "--", "--host"]