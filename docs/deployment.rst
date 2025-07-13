Deployment Guide
===============

This guide covers deploying the Brain Tumor Monitoring System to various environments, from local development to production cloud deployments.

Deployment Options
-----------------

Choose the deployment method that best fits your needs:

* :ref:`local-deployment` - Local development setup
* :ref:`docker-deployment` - Containerized deployment
* :ref:`cloud-deployment` - Cloud platform deployment
* :ref:`kubernetes-deployment` - Kubernetes orchestration

.. _local-deployment:

Local Development Deployment
---------------------------

**Prerequisites:**
* Python 3.8+
* PostgreSQL 12+
* Node.js 16+
* Git

**Step 1: Environment Setup**
.. code-block:: bash

   # Clone repository
   git clone https://github.com/your-org/brain-tumor-monitoring.git
   cd brain-tumor-monitoring

   # Create virtual environment
   python -m venv env
   source env/bin/activate  # Windows: env\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements_dev.txt

**Step 2: Database Setup**
.. code-block:: bash

   # Install PostgreSQL (Ubuntu)
   sudo apt update
   sudo apt install postgresql postgresql-contrib

   # Start PostgreSQL
   sudo systemctl start postgresql
   sudo systemctl enable postgresql

   # Create database and user
   sudo -u postgres psql
   CREATE DATABASE monitoring;
   CREATE USER monitoring_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE monitoring TO monitoring_user;
   \q

**Step 3: Environment Configuration**
.. code-block:: bash

   # Create .env file
   cat > .env << EOF
   DATABASE_URL=postgresql://monitoring_user:your_password@localhost:5432/monitoring
   API_HOST=0.0.0.0
   API_PORT=8000
   DRIFT_THRESHOLD=1.0
   REPORTS_DIR=reports/monitoring
   DEBUG=True
   LOG_LEVEL=INFO
   EOF

**Step 4: Start Services**
.. code-block:: bash

   # Start backend
   uvicorn backend.src.api:app --reload --host 0.0.0.0 --port 8000

   # In another terminal, start frontend
   cd frontend
   npm install
   npm start

**Step 5: Verify Deployment**
.. code-block:: bash

   # Test API
   curl http://localhost:8000/health

   # Test frontend
   open http://localhost:3000

.. _docker-deployment:

Docker Deployment
----------------

**Prerequisites:**
* Docker and Docker Compose
* Git

**Step 1: Clone and Configure**
.. code-block:: bash

   git clone https://github.com/your-org/brain-tumor-monitoring.git
   cd brain-tumor-monitoring

   # Copy environment file
   cp .env.example .env

   # Edit environment variables
   nano .env

**Step 2: Build and Start**
.. code-block:: bash

   # Build and start all services
   docker-compose up -d --build

   # Check service status
   docker-compose ps

   # View logs
   docker-compose logs -f

**Step 3: Verify Deployment**
.. code-block:: bash

   # Test API
   curl http://localhost:8000/health

   # Test frontend
   open http://localhost:3000

   # Check database
   docker-compose exec db psql -U monitoring_user -d monitoring -c "SELECT COUNT(*) FROM predictions_log;"

**Docker Compose Configuration:**
.. code-block:: yaml

   # docker-compose.yml
   version: '3.8'

   services:
     api:
       build:
         context: .
         dockerfile: dockerfiles/api.Dockerfile
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql://monitoring_user:password@db:5432/monitoring
       depends_on:
         - db
       volumes:
         - ./reports:/app/reports
       restart: unless-stopped

     frontend:
       build:
         context: ./frontend
         dockerfile: ../dockerfiles/frontend.Dockerfile
       ports:
         - "3000:3000"
       environment:
         - REACT_APP_API_URL=http://localhost:8000
       depends_on:
         - api
       restart: unless-stopped

     db:
       image: postgres:13
       environment:
         - POSTGRES_DB=monitoring
         - POSTGRES_USER=monitoring_user
         - POSTGRES_PASSWORD=password
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"
       restart: unless-stopped

   volumes:
     postgres_data:

.. _cloud-deployment:

Cloud Deployment
---------------

### Google Cloud Platform (GCP)

**Prerequisites:**
* Google Cloud SDK
* Docker
* GCP project with billing enabled

**Step 1: Setup GCP**
.. code-block:: bash

   # Install Google Cloud SDK
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init

   # Set project
   gcloud config set project YOUR_PROJECT_ID

   # Enable required APIs
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com

**Step 2: Deploy to Cloud Run**
.. code-block:: bash

   # Build and push image
   docker build -t gcr.io/YOUR_PROJECT_ID/brain-tumor-monitoring:latest .
   docker push gcr.io/YOUR_PROJECT_ID/brain-tumor-monitoring:latest

   # Deploy to Cloud Run
   gcloud run deploy brain-tumor-monitoring \
     --image gcr.io/YOUR_PROJECT_ID/brain-tumor-monitoring:latest \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --memory 1Gi \
     --cpu 1 \
     --set-env-vars DATABASE_URL="postgresql://user:password@host:5432/database"

**Step 3: Setup Cloud SQL**
.. code-block:: bash

   # Create Cloud SQL instance
   gcloud sql instances create monitoring-db \
     --database-version=POSTGRES_13 \
     --tier=db-f1-micro \
     --region=us-central1

   # Create database
   gcloud sql databases create monitoring --instance=monitoring-db

   # Create user
   gcloud sql users create monitoring_user \
     --instance=monitoring-db \
     --password=your_password

### Amazon Web Services (AWS)

**Prerequisites:**
* AWS CLI
* Docker
* AWS account

**Step 1: Setup AWS**
.. code-block:: bash

   # Install AWS CLI
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install

   # Configure AWS
   aws configure

**Step 2: Deploy to ECS**
.. code-block:: bash

   # Create ECR repository
   aws ecr create-repository --repository-name brain-tumor-monitoring

   # Build and push image
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
   docker build -t brain-tumor-monitoring .
   docker tag brain-tumor-monitoring:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/brain-tumor-monitoring:latest
   docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/brain-tumor-monitoring:latest

   # Deploy to ECS
   aws ecs create-service \
     --cluster your-cluster \
     --service-name brain-tumor-monitoring \
     --task-definition brain-tumor-monitoring:1 \
     --desired-count 2

### Microsoft Azure

**Prerequisites:**
* Azure CLI
* Docker
* Azure subscription

**Step 1: Setup Azure**
.. code-block:: bash

   # Install Azure CLI
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

   # Login to Azure
   az login

**Step 2: Deploy to Azure Container Instances**
.. code-block:: bash

   # Create resource group
   az group create --name brain-tumor-monitoring --location eastus

   # Create container registry
   az acr create --resource-group brain-tumor-monitoring --name yourregistry --sku Basic

   # Build and push image
   az acr build --registry yourregistry --image brain-tumor-monitoring .

   # Deploy to ACI
   az container create \
     --resource-group brain-tumor-monitoring \
     --name brain-tumor-monitoring \
     --image yourregistry.azurecr.io/brain-tumor-monitoring:latest \
     --dns-name-label brain-tumor-monitoring \
     --ports 8000

.. _kubernetes-deployment:

Kubernetes Deployment
--------------------

**Prerequisites:**
* kubectl
* Docker
* Kubernetes cluster

**Step 1: Create Kubernetes Manifests**
.. code-block:: yaml

   # k8s/deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: brain-tumor-monitoring
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: brain-tumor-monitoring
     template:
       metadata:
         labels:
           app: brain-tumor-monitoring
       spec:
         containers:
         - name: api
           image: your-registry/brain-tumor-monitoring:latest
           ports:
           - containerPort: 8000
           env:
           - name: DATABASE_URL
             valueFrom:
               secretKeyRef:
                 name: monitoring-secrets
                 key: database-url
           resources:
             requests:
               memory: "512Mi"
               cpu: "250m"
             limits:
               memory: "1Gi"
               cpu: "500m"
         - name: frontend
           image: your-registry/brain-tumor-frontend:latest
           ports:
           - containerPort: 3000
           env:
           - name: REACT_APP_API_URL
             value: "http://api:8000"
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: brain-tumor-monitoring-service
   spec:
     selector:
       app: brain-tumor-monitoring
     ports:
     - protocol: TCP
       port: 80
       targetPort: 8000
     type: LoadBalancer

**Step 2: Deploy to Kubernetes**
.. code-block:: bash

   # Create namespace
   kubectl create namespace brain-tumor-monitoring

   # Apply manifests
   kubectl apply -f k8s/

   # Check deployment
   kubectl get pods -n brain-tumor-monitoring
   kubectl get services -n brain-tumor-monitoring

**Step 3: Setup Ingress**
.. code-block:: yaml

   # k8s/ingress.yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: brain-tumor-monitoring-ingress
     annotations:
       nginx.ingress.kubernetes.io/rewrite-target: /
   spec:
     rules:
     - host: your-domain.com
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: brain-tumor-monitoring-service
               port:
                 number: 80

Production Configuration
-----------------------

**Environment Variables:**
.. code-block:: bash

   # Production environment variables
   DATABASE_URL=postgresql://user:password@host:5432/database
   API_HOST=0.0.0.0
   API_PORT=8000
   DRIFT_THRESHOLD=1.0
   REPORTS_DIR=/app/reports
   DEBUG=False
   LOG_LEVEL=WARNING
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=your-domain.com
   CORS_ORIGINS=https://your-domain.com

**Security Configuration:**
.. code-block:: python

   # Security settings
   SECURITY_CONFIG = {
       "CORS_ORIGINS": ["https://your-domain.com"],
       "ALLOWED_HOSTS": ["your-domain.com"],
       "SECURE_SSL_REDIRECT": True,
       "SESSION_COOKIE_SECURE": True,
       "CSRF_COOKIE_SECURE": True,
   }

**Database Configuration:**
.. code-block:: python

   # Database settings
   DATABASE_CONFIG = {
       "pool_size": 20,
       "max_overflow": 30,
       "pool_timeout": 30,
       "pool_recycle": 3600,
   }

**Monitoring Configuration:**
.. code-block:: python

   # Monitoring settings
   MONITORING_CONFIG = {
       "drift_threshold": 1.0,
       "reference_days": 30,
       "current_days": 7,
       "report_retention_days": 30,
   }

Load Balancing
--------------

**Nginx Configuration:**
.. code-block:: nginx

   # nginx.conf
   upstream api_backend {
       server api1:8000;
       server api2:8000;
       server api3:8000;
   }

   upstream frontend_backend {
       server frontend1:3000;
       server frontend2:3000;
   }

   server {
       listen 80;
       server_name your-domain.com;

       location /api/ {
           proxy_pass http://api_backend;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location / {
           proxy_pass http://frontend_backend;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }

**HAProxy Configuration:**
.. code-block:: haproxy

   # haproxy.cfg
   global
       log stdout format raw local0 info

   defaults
       mode http
       timeout connect 5000ms
       timeout client 50000ms
       timeout server 50000ms

   frontend http_front
       bind *:80
       default_backend http_back

   backend http_back
       balance roundrobin
       server api1 api1:8000 check
       server api2 api2:8000 check
       server api3 api3:8000 check

SSL/TLS Configuration
---------------------

**Let's Encrypt Setup:**
.. code-block:: bash

   # Install Certbot
   sudo apt install certbot python3-certbot-nginx

   # Obtain certificate
   sudo certbot --nginx -d your-domain.com

   # Auto-renewal
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet

**Manual SSL Certificate:**
.. code-block:: nginx

   # SSL configuration
   server {
       listen 443 ssl http2;
       server_name your-domain.com;

       ssl_certificate /path/to/certificate.crt;
       ssl_certificate_key /path/to/private.key;

       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
       ssl_prefer_server_ciphers off;
   }

Monitoring & Logging
-------------------

**Prometheus Configuration:**
.. code-block:: yaml

   # prometheus.yml
   global:
     scrape_interval: 15s

   scrape_configs:
     - job_name: 'brain-tumor-monitoring'
       static_configs:
         - targets: ['api:8000']
       metrics_path: '/metrics'
       scrape_interval: 5s

**Grafana Dashboard:**
.. code-block:: json

   {
     "dashboard": {
       "title": "Brain Tumor Monitoring",
       "panels": [
         {
           "title": "API Response Time",
           "type": "graph",
           "targets": [
             {
               "expr": "rate(http_request_duration_seconds_sum[5m])"
             }
           ]
         }
       ]
     }
   }

**Logging Configuration:**
.. code-block:: python

   # logging.conf
   [loggers]
   keys=root,brain_tumor_monitoring

   [handlers]
   keys=consoleHandler,fileHandler

   [formatters]
   keys=normalFormatter

   [logger_root]
   level=INFO
   handlers=consoleHandler

   [logger_brain_tumor_monitoring]
   level=DEBUG
   handlers=consoleHandler,fileHandler
   qualname=brain_tumor_monitoring
   propagate=0

Backup & Recovery
-----------------

**Database Backup:**
.. code-block:: bash

   # Automated backup script
   #!/bin/bash
   BACKUP_DIR="/backups"
   DATE=$(date +%Y%m%d_%H%M%S)

   pg_dump -h localhost -U monitoring_user monitoring > $BACKUP_DIR/backup_$DATE.sql

   # Keep only last 7 days of backups
   find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete

**File Backup:**
.. code-block:: bash

   # Backup reports and configurations
   tar -czf /backups/reports_$(date +%Y%m%d).tar.gz /app/reports
   tar -czf /backups/config_$(date +%Y%m%d).tar.gz /app/config

**Recovery Process:**
.. code-block:: bash

   # Database recovery
   psql -h localhost -U monitoring_user monitoring < backup_20250113_120000.sql

   # File recovery
   tar -xzf reports_20250113.tar.gz -C /app/
   tar -xzf config_20250113.tar.gz -C /app/

CI/CD Pipeline
--------------

**GitHub Actions:**
.. code-block:: yaml

   # .github/workflows/deploy.yml
   name: Deploy to Production

   on:
     push:
       branches: [main]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: 3.10
         - name: Install dependencies
           run: |
             pip install -r requirements.txt
             pip install -r requirements_dev.txt
         - name: Run tests
           run: |
             pytest tests/

     build:
       needs: test
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Build Docker image
           run: |
             docker build -t brain-tumor-monitoring .
         - name: Push to registry
           run: |
             docker tag brain-tumor-monitoring your-registry/brain-tumor-monitoring:latest
             docker push your-registry/brain-tumor-monitoring:latest

     deploy:
       needs: build
       runs-on: ubuntu-latest
       steps:
         - name: Deploy to production
           run: |
             # Deployment commands

**GitLab CI:**
.. code-block:: yaml

   # .gitlab-ci.yml
   stages:
     - test
     - build
     - deploy

   test:
     stage: test
     image: python:3.10
     script:
       - pip install -r requirements.txt
       - pip install -r requirements_dev.txt
       - pytest tests/

   build:
     stage: build
     image: docker:latest
     services:
       - docker:dind
     script:
       - docker build -t brain-tumor-monitoring .
       - docker push your-registry/brain-tumor-monitoring:latest

   deploy:
     stage: deploy
     script:
       - kubectl set image deployment/brain-tumor-monitoring brain-tumor-monitoring=your-registry/brain-tumor-monitoring:latest

Troubleshooting
--------------

**Common Deployment Issues:**

**Database Connection Failed:**
.. code-block:: bash

   # Check database connectivity
   psql -h your-db-host -U your-user -d your-database -c "SELECT 1;"

   # Check network connectivity
   telnet your-db-host 5432

   # Check firewall rules
   sudo ufw status

**Container Won't Start:**
.. code-block:: bash

   # Check container logs
   docker logs container-name

   # Check resource usage
   docker stats

   # Check environment variables
   docker exec container-name env

**Kubernetes Pod Issues:**
.. code-block:: bash

   # Check pod status
   kubectl get pods

   # Check pod logs
   kubectl logs pod-name

   # Check pod events
   kubectl describe pod pod-name

**Load Balancer Issues:**
.. code-block:: bash

   # Check service health
   curl -I http://your-domain.com/health

   # Check load balancer logs
   kubectl logs -n ingress-nginx deployment/ingress-nginx-controller

**Performance Issues:**
.. code-block:: bash

   # Check resource usage
   top
   htop

   # Check database performance
   pg_stat_statements

   # Check network latency
   ping your-domain.com

For detailed troubleshooting, see :doc:`troubleshooting`.

For monitoring setup, see :doc:`monitoring/index`.
