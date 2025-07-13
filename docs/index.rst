Brain Tumor Monitoring System Documentation
==========================================

Welcome to the comprehensive documentation for the Brain Tumor Monitoring System, a sophisticated MLOps solution for monitoring and detecting data drift in brain tumor image classification models.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   quickstart
   architecture
   api/index
   monitoring/index
   ml/index
   frontend/index
   deployment
   troubleshooting
   contributing

.. image:: _static/images/system-overview.png
   :alt: System Architecture Overview
   :align: center
   :width: 800px

Overview
--------

The Brain Tumor Monitoring System is designed to provide comprehensive monitoring capabilities for machine learning models that classify brain tumor images. The system includes:

* **Real-time Monitoring**: Continuous monitoring of model predictions and data quality
* **Drift Detection**: Advanced algorithms to detect data drift in image features
* **Automated Reporting**: HTML reports with visualizations using Evidently AI
* **RESTful API**: FastAPI-based backend with comprehensive endpoints
* **Modern Frontend**: React-based dashboard with real-time updates
* **Cloud Deployment**: Ready for deployment on GCP, AWS, or Azure

Key Features
------------

* **Image Feature Extraction**: Comprehensive feature extraction from brain tumor images
* **Statistical Analysis**: Mean, standard deviation, entropy, and other statistical measures
* **Drift Detection**: Customizable thresholds for detecting significant data drift
* **Dashboard**: Real-time monitoring dashboard with key metrics
* **API Integration**: Seamless integration with existing ML pipelines
* **Scalable Architecture**: Designed for production deployment

Quick Start
-----------

.. code-block:: bash

   # Clone the repository
   git clone <repository-url>
   cd brain-tumor-monitoring

   # Install dependencies
   pip install -r requirements.txt

   # Set up database
   export DATABASE_URL="postgresql://user:password@localhost:5432/monitoring"

   # Run the backend
   uvicorn backend.src.api:app --reload

   # Run the frontend
   cd frontend && npm install && npm start

For detailed installation instructions, see :doc:`installation`.

API Reference
-------------

The system provides a comprehensive REST API for monitoring operations:

* **Health Checks**: `/health`
* **Monitoring Dashboard**: `/monitoring/dashboard`
* **Drift Reports**: `/monitoring/drift-report`
* **Feature Analysis**: `/monitoring/feature-analysis`
* **Data Quality**: `/monitoring/data-quality`

For complete API documentation, see :doc:`api/index`.

Monitoring System
----------------

The monitoring system provides:

* **Feature Extraction**: Automatic extraction of image features
* **Drift Detection**: Statistical analysis for data drift
* **Reporting**: HTML reports with visualizations
* **Alerting**: Configurable alerts for drift detection

For detailed monitoring documentation, see :doc:`monitoring/index`.

Machine Learning
---------------

The ML pipeline includes:

* **Model Training**: YOLOv8-based tumor detection
* **Prediction Pipeline**: Real-time image classification
* **Feature Engineering**: Comprehensive feature extraction
* **Model Versioning**: Version control for ML models

For ML documentation, see :doc:`ml/index`.

Frontend Dashboard
-----------------

The React-based frontend provides:

* **Real-time Monitoring**: Live updates of system metrics
* **Interactive Charts**: Visual representation of drift data
* **Report Viewer**: HTML report display
* **Responsive Design**: Mobile-friendly interface

For frontend documentation, see :doc:`frontend/index`.

Deployment
----------

The system supports multiple deployment options:

* **Local Development**: Docker Compose setup
* **Cloud Deployment**: GCP, AWS, Azure support
* **Kubernetes**: Full K8s deployment manifests
* **CI/CD**: Automated deployment pipelines

For deployment instructions, see :doc:`deployment`.

Contributing
-----------

We welcome contributions! Please see :doc:`contributing` for guidelines.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
