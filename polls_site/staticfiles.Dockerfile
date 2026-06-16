FROM ghcr.io/benoitc/gunicorn:26 AS build

# Set up container
WORKDIR /backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

# Collect backend' static files
COPY --chown=gunicorn:gunicorn . .
RUN python manage.py collectstatic

FROM nginx:1.31

# Copy server config and files to be served
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /backend/backend-static /usr/share/nginx/html/backend-static
