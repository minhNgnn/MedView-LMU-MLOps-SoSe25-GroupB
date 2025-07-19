FROM prom/prometheus:v2.52.0

# Copy your Prometheus config into the image
COPY monitoring/prometheus.yaml /etc/prometheus/prometheus.yaml
