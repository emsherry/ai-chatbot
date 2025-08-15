# -----------------
# Backend stage
# -----------------
FROM python:3.9-slim as backend

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# -----------------
# Frontend stage
# -----------------
FROM node:16-alpine as frontend

WORKDIR /app
COPY frontend/package*.json ./

# Install **all dependencies** (dev + prod)
RUN npm ci

COPY frontend/ .
RUN npm run build

# -----------------
# Nginx production stage
# -----------------
FROM nginx:alpine
COPY --from=frontend /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
