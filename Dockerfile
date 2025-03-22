# Build stage
FROM python:3.12-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y \
        redis-server \
        supervisor \
        curl \
        gettext-base && \
    # Install Caddy from GitHub releases
    curl -o /usr/local/bin/caddy -L "https://github.com/caddyserver/caddy/releases/download/v2.7.5/caddy_2.7.5_linux_amd64" && \
    chmod +x /usr/local/bin/caddy && \
    # Cleanup
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
WORKDIR /app
COPY . .

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create Caddy config directory
RUN mkdir -p /etc/caddy

# Copy Caddy config and entrypoint
COPY Caddyfile.template /etc/caddy/
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

# Expose only HTTP/HTTPS ports
EXPOSE 80 443

# Run supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

ENTRYPOINT ["/docker-entrypoint.sh"]