System Architecture
==================

This document provides a detailed overview of the Brain Tumor Monitoring System architecture, including components, data flow, and design decisions.

High-Level Architecture
----------------------

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

.. code-block:: text

   monitoring/
   └── core/
       ├── monitor.py           # Main monitor class, orchestrates monitoring logic
       ├── drift_detector.py    # Drift detection logic
       ├── feature_extractor.py # Feature extraction
       └── __init__.py          # Core monitoring package init

   # Monitoring logic is now integrated into the backend (see backend/src/api.py)

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
