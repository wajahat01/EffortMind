# Stage 1: Build React frontend
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Set up Python backend
FROM python:3.10-slim AS backend-build
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./

# Stage 3: Final image with Nginx and Flask
FROM nginx:alpine

# Copy Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy React build to Nginx html directory
COPY --from=frontend-build /app/frontend/build /usr/share/nginx/html

# Copy backend code
COPY --from=backend-build /app/backend /app/backend

# Install Python and dependencies for Flask
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir -r /app/backend/requirements.txt

# Expose ports (80 for Nginx, 5000 for Flask)
EXPOSE 80 5000

# Start both Flask and Nginx
CMD ["/bin/sh", "-c", "python3 /app/backend/app.py & nginx -g 'daemon off;'"] 