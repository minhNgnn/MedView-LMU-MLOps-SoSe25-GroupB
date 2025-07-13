System Architecture
==================

This document provides a detailed overview of the Brain Tumor Monitoring System architecture, including components, data flow, and design decisions.

High-Level Architecture
----------------------

.. image:: _static/images/system-architecture.png
   :alt: System Architecture Overview
   :align: center
   :width: 800px

The system follows a microservices architecture with the following key components:

**Frontend Layer**
    React-based dashboard providing real-time monitoring interface

**API Gateway**
    FastAPI-based REST API handling all client requests

**Monitoring Engine**
    Core monitoring logic for drift detection and feature extraction

**Database Layer**
    PostgreSQL database storing predictions, features, and monitoring data

**ML Pipeline**
    YOLOv8-based brain tumor detection and classification

**Reporting System**
    Evidently AI-powered HTML report generation

Component Details
----------------

Frontend (React + TypeScript)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Technology Stack:**
* React 18+ with TypeScript
* Tailwind CSS for styling
* Chart.js for visualizations
* React Router for navigation
* Axios for API communication

**Key Features:**
* Real-time dashboard updates
* Interactive charts and graphs
* Image upload interface
* Report viewer
* Responsive design

**Architecture:**

.. code-block:: typescript

   // Component structure
   src/
   ├── components/          # Reusable UI components
   │   ├── Dashboard.tsx   # Main dashboard
   │   ├── Upload.tsx      # Image upload
   │   └── Reports.tsx     # Report viewer
   ├── hooks/              # Custom React hooks
   ├── pages/              # Page components
   ├── types/              # TypeScript definitions
   └── utils/              # Utility functions

Backend API (FastAPI)
^^^^^^^^^^^^^^^^^^^^

**Technology Stack:**
* FastAPI for REST API
* SQLAlchemy for ORM
* PostgreSQL for database
* Pydantic for data validation
* Uvicorn for ASGI server

**API Structure:**

.. code-block:: python

   backend/
   ├── src/
   │   └── api.py         # Main FastAPI application
   ├── migrations/         # Database migrations
   └── requirements.txt    # Python dependencies

**Key Endpoints:**
* `/health` - Health checks
* `/predict` - Image prediction
* `/monitoring/*` - Monitoring endpoints
* `/patients/*` - Patient management

Monitoring Engine
^^^^^^^^^^^^^^^^

**Core Components:**
* **BrainTumorImageMonitor**: Main orchestrator
* **DriftDetector**: Statistical drift detection
* **FeatureExtractor**: Image feature extraction
* **ReportGenerator**: HTML report creation

**Architecture:**

.. code-block:: python

   monitoring/
   ├── core/
   │   ├── monitor.py        # Main monitor class
   │   ├── drift_detector.py # Drift detection logic
   │   └── feature_extractor.py # Feature extraction
   ├── api/
   │   └── main.py          # Standalone monitoring API
   └── tests/               # Unit tests

Database Design
^^^^^^^^^^^^^^

**PostgreSQL Schema:**

.. code-block:: sql

   -- Main predictions table
   CREATE TABLE predictions_log (
       id SERIAL PRIMARY KEY,
       timestamp TIMESTAMP NOT NULL,
       prediction_confidence FLOAT,
       prediction_class VARCHAR(50),
       num_detections INTEGER,
       model_version VARCHAR(50),
       processing_time_ms INTEGER,

       -- Image features
       image_width INTEGER,
       image_height INTEGER,
       image_channels INTEGER,
       image_size_bytes BIGINT,
       brightness_mean FLOAT,
       brightness_std FLOAT,
       contrast_mean FLOAT,
       contrast_std FLOAT,
       entropy FLOAT,
       skewness FLOAT,
       kurtosis FLOAT,
       mean_intensity FLOAT,
       std_intensity FLOAT,

       -- Tumor-specific features
       tumor_area_ratio FLOAT,
       tumor_detection_confidence FLOAT,
       num_tumors_detected INTEGER,
       largest_tumor_area FLOAT,
       tumor_density FLOAT,
       tumor_location_x FLOAT,
       tumor_location_y FLOAT,
       tumor_shape_regularity FLOAT
   );

**Indexes:**

.. code-block:: sql

   -- Performance indexes
   CREATE INDEX idx_predictions_timestamp ON predictions_log(timestamp);
   CREATE INDEX idx_predictions_class ON predictions_log(prediction_class);
   CREATE INDEX idx_predictions_confidence ON predictions_log(prediction_confidence);

ML Pipeline
^^^^^^^^^^^

**Technology Stack:**
* YOLOv8 for object detection
* OpenCV for image processing
* NumPy/Pandas for data manipulation
* PyTorch for deep learning

**Pipeline Components:**

.. code-block:: python

   ml/
   ├── train.py           # Model training
   ├── predict.py         # Model inference
   ├── models.py          # Model definitions
   ├── configs/           # Configuration files
   └── utils.py           # Utility functions

**Training Process:**
1. **Data Preparation**: Image preprocessing and annotation
2. **Model Training**: YOLOv8 training with custom dataset
3. **Validation**: Model evaluation on test set
4. **Export**: Model export for production

**Inference Process:**
1. **Image Preprocessing**: Resize, normalize, format conversion
2. **Model Inference**: YOLOv8 prediction
3. **Post-processing**: NMS, confidence filtering
4. **Feature Extraction**: Statistical and tumor-specific features

Data Flow
---------

**Image Upload Flow:**
.. mermaid::

   graph TD
       A[User Uploads Image] --> B[API Gateway]
       B --> C[Image Validation]
       C --> D[ML Model Inference]
       D --> E[Feature Extraction]
       E --> F[Database Storage]
       F --> G[Response to User]
       G --> H[Background Monitoring]

**Monitoring Flow:**
.. mermaid::

   graph TD
       A[New Prediction] --> B[Feature Extraction]
       B --> C[Database Storage]
       C --> D[Drift Analysis]
       D --> E[Report Generation]
       E --> F[Dashboard Update]
       F --> G[Alert System]

**Drift Detection Flow:**
.. mermaid::

   graph TD
       A[Reference Data] --> B[Statistical Analysis]
       C[Current Data] --> B
       B --> D[Drift Scoring]
       D --> E[Threshold Check]
       E --> F[Alert Generation]
       F --> G[Report Creation]

Security Architecture
--------------------

**Authentication & Authorization:**
* JWT token-based authentication
* Role-based access control (RBAC)
* API key management
* Session management

**Data Security:**
* HTTPS/TLS encryption
* Database encryption at rest
* Secure file upload validation
* Input sanitization

**Network Security:**
* CORS configuration
* Rate limiting
* DDoS protection
* Firewall rules

**Compliance:**
* HIPAA compliance for medical data
* GDPR compliance for EU users
* Data retention policies
* Audit logging

Scalability Design
-----------------

**Horizontal Scaling:**
* Stateless API design
* Load balancer support
* Database connection pooling
* Microservices architecture

**Vertical Scaling:**
* Resource monitoring
* Auto-scaling policies
* Performance optimization
* Caching strategies

**Database Scaling:**
* Read replicas
* Connection pooling
* Query optimization
* Partitioning strategies

**Caching Strategy:**
* Redis for session storage
* CDN for static assets
* Browser caching
* API response caching

Performance Optimization
----------------------

**API Performance:**
* Async/await patterns
* Background task processing
* Database query optimization
* Response compression

**Frontend Performance:**
* Code splitting
* Lazy loading
* Image optimization
* Bundle optimization

**Database Performance:**
* Index optimization
* Query optimization
* Connection pooling
* Read/write separation

**Monitoring Performance:**
* Efficient feature extraction
* Batch processing
* Caching strategies
* Parallel processing

Deployment Architecture
----------------------

**Development Environment:**

.. code-block:: yaml

   # docker-compose.yml
   version: '3.8'
   services:
     api:
       build: ./backend
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql://user:pass@db:5432/monitoring
       depends_on:
         - db

     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
       depends_on:
         - api

     db:
       image: postgres:13
       environment:
         - POSTGRES_DB=monitoring
         - POSTGRES_USER=user
         - POSTGRES_PASSWORD=pass
       volumes:
         - postgres_data:/var/lib/postgresql/data

**Production Environment:**
* **Cloud Deployment**: GCP, AWS, Azure support
* **Container Orchestration**: Kubernetes, Docker Swarm
* **Load Balancing**: Nginx, HAProxy, Cloud Load Balancer
* **Monitoring**: Prometheus, Grafana, Cloud Monitoring

**CI/CD Pipeline:**

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
         - name: Run tests
           run: |
             pip install -r requirements.txt
             pytest tests/

     deploy:
       needs: test
       runs-on: ubuntu-latest
       steps:
         - name: Deploy to Cloud
           run: |
             # Deployment steps

Error Handling
--------------

**API Error Handling:**
* Global exception handlers
* Structured error responses
* Logging and monitoring
* Graceful degradation

**Database Error Handling:**
* Connection retry logic
* Transaction rollback
* Deadlock detection
* Query timeout handling

**Monitoring Error Handling:**
* Feature extraction fallbacks
* Drift detection error recovery
* Report generation error handling
* Alert system redundancy

**Frontend Error Handling:**
* Error boundaries
* Network error handling
* User-friendly error messages
* Retry mechanisms

Monitoring & Observability
-------------------------

**Application Monitoring:**
* Request/response logging
* Performance metrics
* Error tracking
* User behavior analytics

**Infrastructure Monitoring:**
* System resource usage
* Database performance
* Network latency
* Service health checks

**Business Metrics:**
* Prediction accuracy
* Drift detection rates
* User engagement
* System uptime

**Alerting:**
* Performance thresholds
* Error rate alerts
* Drift detection alerts
* System health alerts

Integration Points
-----------------

**External APIs:**
* Medical imaging systems
* Electronic health records
* Laboratory information systems
* Telemedicine platforms

**Data Sources:**
* PACS systems
* DICOM servers
* Cloud storage
* Local file systems

**Third-party Services:**
* Authentication providers
* Email services
* SMS services
* Cloud monitoring

**ML Pipeline Integration:**
* Model training pipelines
* Feature stores
* Model registries
* Experiment tracking

Future Architecture
------------------

**Planned Enhancements:**
* GraphQL API support
* Real-time streaming
* Advanced ML models
* Mobile applications

**Scalability Improvements:**
* Event-driven architecture
* Message queues
* Distributed caching
* Multi-region deployment

**Security Enhancements:**
* Zero-trust architecture
* Advanced encryption
* Compliance automation
* Security monitoring

**Performance Optimizations:**
* Edge computing
* CDN integration
* Database sharding
* Microservices decomposition

For detailed implementation information, see:
* :doc:`api/index` - API architecture details
* :doc:`monitoring/index` - Monitoring system architecture
* :doc:`deployment` - Deployment architecture
* :doc:`troubleshooting` - Architecture troubleshooting
