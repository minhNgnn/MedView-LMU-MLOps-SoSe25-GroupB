Installation Guide
=================

This guide will walk you through installing and setting up the Brain Tumor Monitoring System on your local machine or server.

Prerequisites
------------

**System Requirements**
    * Python 3.8 or higher
    * Node.js 16 or higher (for frontend)
    * PostgreSQL 12 or higher
    * Docker and Docker Compose (optional, for containerized setup)

**Operating Systems**
    * Linux (Ubuntu 20.04+, CentOS 8+)
    * macOS (10.15+)
    * Windows 10/11 (with WSL2 recommended)

**Hardware Requirements**
    * CPU: 4+ cores recommended
    * RAM: 8GB minimum, 16GB recommended
    * Storage: 20GB free space
    * GPU: Optional, for ML model inference acceleration

Installation Methods
-------------------

Choose the installation method that best fits your needs:

* :ref:`local-installation` - Direct installation on your system
* :ref:`docker-installation` - Containerized installation with Docker
* :ref:`cloud-installation` - Cloud deployment options

.. _local-installation:

Local Installation
-----------------

**Step 1: Clone the Repository**

.. code-block:: bash

   git clone https://github.com/your-org/brain-tumor-monitoring.git
   cd brain-tumor-monitoring

**Step 2: Set Up Python Environment**

.. code-block:: bash

   # Create virtual environment
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

   # Install Python dependencies
   pip install -r requirements.txt
   pip install -r requirements_dev.txt  # For development

**Step 3: Install Node.js Dependencies**

.. code-block:: bash

   cd frontend
   npm install
   cd ..

**Step 4: Set Up PostgreSQL Database**

Install PostgreSQL on your system:

**Ubuntu/Debian:**
.. code-block:: bash

   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   sudo systemctl enable postgresql

**macOS:**
.. code-block:: bash

   brew install postgresql
   brew services start postgresql

**Windows:**
Download and install from `https://www.postgresql.org/download/windows/`

**Create Database and User:**

.. code-block:: bash

   sudo -u postgres psql

   CREATE DATABASE monitoring;
   CREATE USER monitoring_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE monitoring TO monitoring_user;
   \q

**Step 5: Run Database Migrations**

.. code-block:: bash

   # Set environment variable
   export DATABASE_URL="postgresql://monitoring_user:your_password@localhost:5432/monitoring"

   # Run migrations
   python backend/migrations/create_monitoring_tables.sql

**Step 6: Configure Environment Variables**

Create a `.env` file in the project root:

.. code-block:: bash

   # Database configuration
   DATABASE_URL=postgresql://monitoring_user:your_password@localhost:5432/monitoring

   # API configuration
   API_HOST=0.0.0.0
   API_PORT=8000

   # Monitoring configuration
   DRIFT_THRESHOLD=1.0
   REPORTS_DIR=reports/monitoring

   # Development settings
   DEBUG=True
   LOG_LEVEL=INFO

**Step 7: Verify Installation**

.. code-block:: bash

   # Test backend
   uvicorn backend.src.api:app --reload --host 0.0.0.0 --port 8000

   # In another terminal, test frontend
   cd frontend
   npm start

.. _docker-installation:

Docker Installation
------------------

**Step 1: Install Docker and Docker Compose**

**Ubuntu/Debian:**
.. code-block:: bash

   sudo apt update
   sudo apt install docker.io docker-compose
   sudo usermod -aG docker $USER
   newgrp docker

**macOS:**
Download Docker Desktop from `https://www.docker.com/products/docker-desktop`

**Windows:**
Download Docker Desktop from `https://www.docker.com/products/docker-desktop`

**Step 2: Clone and Configure**

.. code-block:: bash

   git clone https://github.com/your-org/brain-tumor-monitoring.git
   cd brain-tumor-monitoring

   # Copy environment file
   cp .env.example .env

   # Edit .env file with your configuration
   nano .env

**Step 3: Start Services**

.. code-block:: bash

   # Start all services
   docker-compose up -d

   # View logs
   docker-compose logs -f

**Step 4: Verify Installation**

.. code-block:: bash

   # Check service status
   docker-compose ps

   # Test API
   curl http://localhost:8000/health

   # Access frontend
   open http://localhost:3000

.. _cloud-installation:

Cloud Installation
-----------------

**Google Cloud Platform (GCP)**

.. code-block:: bash

   # Install Google Cloud SDK
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   gcloud init

   # Enable required APIs
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com

   # Deploy using provided scripts
   ./monitoring/deploy.sh your-project-id us-central1

**Amazon Web Services (AWS)**

.. code-block:: bash

   # Install AWS CLI
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install

   # Configure AWS credentials
   aws configure

   # Deploy using AWS ECS or EKS

**Microsoft Azure**

.. code-block:: bash

   # Install Azure CLI
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

   # Login to Azure
   az login

   # Deploy using Azure Container Instances or AKS

Configuration
------------

**Database Configuration**

The system supports PostgreSQL with the following configuration options:

.. code-block:: python

   # Example database configuration
   DATABASE_URL = "postgresql://user:password@host:5432/database"

   # Connection pool settings
   DB_POOL_SIZE = 10
   DB_MAX_OVERFLOW = 20
   DB_POOL_TIMEOUT = 30

**Monitoring Configuration**

.. code-block:: python

   # Drift detection settings
   DRIFT_THRESHOLD = 1.0  # Sensitivity for drift detection
   REFERENCE_DAYS = 30    # Days of data for reference set
   CURRENT_DAYS = 7       # Days of data for current set

   # Feature extraction settings
   IMAGE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
   FEATURE_EXTRACTION_TIMEOUT = 30     # seconds

**API Configuration**

.. code-block:: python

   # Server settings
   API_HOST = "0.0.0.0"
   API_PORT = 8000
   API_WORKERS = 4

   # CORS settings
   CORS_ORIGINS = ["http://localhost:3000", "https://your-domain.com"]

   # Rate limiting
   RATE_LIMIT_PER_MINUTE = 100

**Frontend Configuration**

.. code-block:: javascript

   // API endpoint configuration
   const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

   // Dashboard refresh interval (seconds)
   const REFRESH_INTERVAL = 30;

   // Chart configuration
   const CHART_COLORS = {
     primary: '#2980B9',
     secondary: '#E74C3C',
     success: '#27AE60'
   };

Verification
-----------

**Backend Verification**

.. code-block:: bash

   # Test health endpoint
   curl http://localhost:8000/health

   # Test monitoring endpoints
   curl http://localhost:8000/monitoring/dashboard
   curl http://localhost:8000/monitoring/feature-analysis

   # Check API documentation
   open http://localhost:8000/docs

**Frontend Verification**

.. code-block:: bash

   # Start frontend development server
   cd frontend
   npm start

   # Open browser and verify dashboard loads
   open http://localhost:3000

**Database Verification**

.. code-block:: bash

   # Connect to database
   psql -h localhost -U monitoring_user -d monitoring

   # Check tables exist
   \dt

   # Verify monitoring tables
   SELECT COUNT(*) FROM predictions_log;

**ML Pipeline Verification**

.. code-block:: bash

   # Test image prediction
   python ml/predict.py --image path/to/test/image.jpg

   # Test model training
   python ml/train.py --config ml/configs/model/config.yaml

Troubleshooting
--------------

**Common Issues**

**Database Connection Failed**
    * Verify PostgreSQL is running: `sudo systemctl status postgresql`
    * Check connection string format
    * Ensure firewall allows connections
    * Verify user permissions

**API Won't Start**
    * Check port availability: `netstat -tulpn | grep 8000`
    * Verify environment variables are set
    * Check Python dependencies: `pip list`
    * Review logs: `tail -f logs/api.log`

**Frontend Build Fails**
    * Clear node_modules: `rm -rf node_modules && npm install`
    * Check Node.js version: `node --version`
    * Verify npm cache: `npm cache clean --force`

**Docker Issues**
    * Check Docker service: `sudo systemctl status docker`
    * Verify Docker Compose version: `docker-compose --version`
    * Clear Docker cache: `docker system prune -a`

**Performance Issues**
    * Monitor resource usage: `htop` or `top`
    * Check database connection pool
    * Verify memory allocation for containers
    * Review API response times

**Getting Help**

* **Documentation**: Check this documentation for detailed guides
* **Issues**: Report bugs on GitHub Issues
* **Discussions**: Join community discussions
* **Support**: Contact the development team

Next Steps
----------

After successful installation:

1. **Quick Start**: Follow the :doc:`quickstart` guide
2. **API Reference**: Explore the :doc:`api/index` documentation
3. **Monitoring Setup**: Configure monitoring in :doc:`monitoring/index`
4. **Deployment**: Set up production deployment in :doc:`deployment`
