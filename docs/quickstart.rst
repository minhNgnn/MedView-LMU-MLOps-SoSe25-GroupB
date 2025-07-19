Quick Start Guide
================

This guide will help you get the Brain Tumor Monitoring System up and running quickly.

Prerequisites
------------

Before starting, ensure you have:

* Python 3.8+ installed
* PostgreSQL database running
* Node.js 16+ (for frontend)
* Git installed

Step 1: Clone the Repository
---------------------------

.. code-block:: bash

   git clone https://github.com/minhNgnn/MedView-LMU-MLOps-SoSe25-GroupB.git
   cd MedView-LMU-MLOps-SoSe25-GroupB

**Create virtual environment:**

.. code-block:: bash

   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

**Install dependencies:**

.. code-block:: bash

   pip install -r requirements_dev.txt
   # Install backend dependencies
   cd backend
   pip install -r requirements.txt

   # Install ML dependencies
   cd ../ml
   pip install -r requirements.txt

   # (Optional) Install test dependencies
   cd ../tests
   pip install -r requirements_tests.txt

   # (Frontend) Install Node.js dependencies
   cd ../frontend
   npm install

Step 2: Database Setup
----------------------

**Create database:**

.. code-block:: bash

   # Connect to PostgreSQL
   sudo -u postgres psql

   # Create database and user
   CREATE DATABASE monitoring;
   CREATE USER monitoring_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE monitoring TO monitoring_user;
   \q

**Run migrations:**

.. code-block:: bash

   # Set environment variable
   export DATABASE_URL="postgresql://monitoring_user:your_password@localhost:5432/monitoring"

   # Run the migration script
   psql -h localhost -U monitoring_user -d monitoring -f backend/migrations/create_monitoring_tables.sql

.. note::
   The database and user are already provisioned in the cloud. You do **not** need to run the `CREATE DATABASE` or `CREATE USER` commands. You will receive the `DATABASE_URL` from the project maintainer. Add this to your `.env` file as described above.

.. code-block:: bash

   # (No need to run these commands)
   # sudo -u postgres psql
   # CREATE DATABASE monitoring;
   # CREATE USER monitoring_user WITH PASSWORD 'your_password';
   # GRANT ALL PRIVILEGES ON DATABASE monitoring TO monitoring_user;
   # \q

**Run migrations:**

.. code-block:: bash

   # Set environment variable
   export DATABASE_URL="postgresql://monitoring_user:your_password@localhost:5432/monitoring"

   # Run the migration script
   psql -h localhost -U monitoring_user -d monitoring -f backend/migrations/create_monitoring_tables.sql

.. note::
   The actual database credentials (including the cloud DATABASE_URL) will be provided to you securely by the project maintainer. Do not share or commit your `.env` file. To set up your environment, copy `.env.example` to `.env` and fill in the real values:

   .. code-block:: bash

      cp .env.example .env
      # Then edit .env and fill in the real DATABASE_URL

Step 3: Start the Backend
-------------------------

**Set environment variables:**

.. code-block:: bash

   export DATABASE_URL="postgresql://monitoring_user:your_password@localhost:5432/monitoring"
   export DEBUG=True

**Start the API server:**

.. code-block:: bash

   uvicorn backend.src.api:app --reload --host 0.0.0.0 --port 8000

**Verify the backend is running:**

.. code-block:: bash

   curl https://gcp-test-app-351704569398.europe-west1.run.app/health

You should see:

.. code-block:: json

   {
     "status": "ok",
     "message": "Backend is running"
   }

Step 4: Start the Frontend
--------------------------

**Install Node.js dependencies:**

.. code-block:: bash

   cd frontend
   npm install
   cd ..

**Start the frontend development server:**

.. code-block:: bash

   cd frontend
   npm start

The frontend will open automatically at `http://localhost:3000`

Step 5: Test the System
-----------------------

**Upload a test image:**

.. code-block:: bash

   curl -X POST https://gcp-test-app-351704569398.europe-west1.run.app/predict \
     -F "file=@path/to/test/image.jpg"

**Check monitoring dashboard:**

.. code-block:: bash

   curl https://gcp-test-app-351704569398.europe-west1.run.app/monitoring/dashboard

**Generate a drift report:**

.. code-block:: bash

   curl "https://gcp-test-app-351704569398.europe-west1.run.app/monitoring/drift-report?days=7"

Step 6: Explore the Dashboard
----------------------------

Open your browser and navigate to `http://localhost:3000`

You should see:

* **Dashboard**: Real-time monitoring metrics
* **Upload**: Image upload and prediction interface
* **Reports**: Generated drift reports
* **Settings**: System configuration

Step 7: Generate Sample Data
---------------------------

**Create synthetic data for testing:**

.. code-block:: python

   from monitoring.core.monitor import BrainTumorImageMonitor
   import numpy as np

   # Initialize monitor
   monitor = BrainTumorImageMonitor("postgresql://monitoring_user:your_password@localhost:5432/monitoring")

   # Generate synthetic images
   for i in range(100):
       # Create random image
       image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)

       # Create prediction data
       prediction = {
           "confidence": np.random.uniform(0.7, 0.95),
           "class": np.random.choice(["benign", "malignant", "normal"]),
           "num_detections": np.random.randint(0, 3)
       }

       # Log prediction
       monitor.log_prediction(image, prediction)

**Verify data generation:**

.. code-block:: bash

   curl https://gcp-test-app-351704569398.europe-west1.run.app/monitoring/dashboard

Step 8: Test Drift Detection
----------------------------

**Generate drifted data:**

.. code-block:: python

   # Generate data with different characteristics
   for i in range(50):
       # Create brighter images (drift in brightness)
       image = np.random.randint(100, 255, (512, 512, 3), dtype=np.uint8)

       prediction = {
           "confidence": np.random.uniform(0.6, 0.9),
           "class": np.random.choice(["benign", "malignant", "normal"]),
           "num_detections": np.random.randint(0, 3)
       }

       monitor.log_prediction(image, prediction)

**Check drift analysis:**

.. code-block:: bash

   curl "https://gcp-test-app-351704569398.europe-west1.run.app/monitoring/feature-analysis?days=7"

**Generate drift report:**

.. code-block:: bash

   curl "https://gcp-test-app-351704569398.europe-west1.run.app/monitoring/drift-report?days=7"


Step 9: Next Steps
-------------------

**Production Deployment:**

* Follow the :doc:`deployment` guide
* Set up proper authentication
* Configure monitoring and alerting
* Implement backup strategies

**Customization:**

* Adjust drift detection thresholds
* Customize feature extraction
* Modify report templates
* Add custom monitoring metrics

**Integration:**

* Integrate with existing ML pipelines
* Set up automated monitoring
* Configure alerting systems
* Implement CI/CD pipelines

Troubleshooting
--------------

**Common Issues:**

**Backend won't start:**

.. code-block:: bash

   # Check if port is in use
   lsof -i :8000

   # Check environment variables
   echo $DATABASE_URL

   # Check database connection
   psql -h localhost -U monitoring_user -d monitoring -c "SELECT 1;"

**Frontend won't start:**

.. code-block:: bash

   # Check Node.js version
   node --version

   # Clear npm cache
   npm cache clean --force

   # Reinstall dependencies
   rm -rf node_modules package-lock.json
   npm install

**Database connection issues:**

.. code-block:: bash

   # Check PostgreSQL status
   sudo systemctl status postgresql

   # Test connection
   psql -h localhost -U monitoring_user -d monitoring

   # Check logs
   tail -f /var/log/postgresql/postgresql-*.log

**No drift detection:**

* Ensure sufficient data exists (at least 50 records)
* Check drift threshold settings
* Verify feature extraction is working
* Review database data quality

**Getting Help:**

* Check the :doc:`troubleshooting` guide
* Review system logs
* Test with sample data
* Contact the development team

Configuration Options
--------------------

**Environment Variables:**

.. code-block:: bash

   # Database
   export DATABASE_URL="postgresql://user:password@host:5432/database"

   # API settings
   export API_HOST="0.0.0.0"
   export API_PORT="8000"

   # Monitoring settings
   export DRIFT_THRESHOLD="1.0"
   export REPORTS_DIR="reports/monitoring"

   # Development settings
   export DEBUG="True"
   export LOG_LEVEL="INFO"

**Configuration File:**
Create a `.env` file in the project root:

.. code-block:: bash

   # .env file
   DATABASE_URL=postgresql://monitoring_user:your_password@localhost:5432/monitoring
   API_HOST=0.0.0.0
   API_PORT=8000
   DRIFT_THRESHOLD=1.0
   REPORTS_DIR=reports/monitoring
   DEBUG=True
   LOG_LEVEL=INFO

**Docker Setup (Alternative):**

.. code-block:: bash

   # Use Docker Compose for easier setup
   docker-compose up -d

   # Check services
   docker-compose ps

   # View logs
   docker-compose logs -f

What's Next?
-----------

Now that you have the system running, explore:

1. **API Documentation**: Test different endpoints
2. **Monitoring Dashboard**: Explore real-time metrics
3. **Drift Reports**: Generate and analyze reports
4. **Customization**: Adjust settings for your needs
5. **Production Setup**: Deploy to production environment

For detailed information, see:

* :doc:`api/index` - Complete API reference
* :doc:`monitoring/index` - Monitoring system details
* :doc:`deployment` - Production deployment guide
* :doc:`troubleshooting` - Common issues and solutions
