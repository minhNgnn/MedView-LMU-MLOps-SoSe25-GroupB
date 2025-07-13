Monitoring System
================

The Brain Tumor Monitoring System provides comprehensive monitoring capabilities for detecting data drift and ensuring model reliability in medical AI applications.

.. toctree::
   :maxdepth: 2
   :caption: Monitoring Documentation:

   architecture
   features
   drift_detection
   reporting
   configuration
   troubleshooting

Overview
--------

The monitoring system is designed to continuously track the performance and data quality of brain tumor classification models. It provides:

* **Real-time Monitoring**: Live tracking of model predictions and data quality
* **Drift Detection**: Advanced algorithms to detect data and concept drift
* **Automated Reporting**: HTML reports with visualizations for stakeholders
* **Alerting**: Configurable alerts for significant drift detection
* **Historical Analysis**: Trend analysis and performance tracking over time

Key Components
-------------

**Monitoring Engine**
    Core monitoring logic that orchestrates feature extraction, drift detection, and reporting.

**Feature Extractor**
    Extracts comprehensive features from brain tumor images including statistical measures and tumor-specific characteristics.

**Drift Detector**
    Implements statistical algorithms to detect significant changes in data distributions.

**Report Generator**
    Creates HTML reports with interactive visualizations using Evidently AI.

**Dashboard API**
    Provides REST endpoints for real-time monitoring data and alerts.

System Architecture
------------------

.. image:: _static/images/monitoring-architecture.png
   :alt: Monitoring System Architecture
   :align: center
   :width: 600px

The monitoring system follows a modular architecture:

**Data Flow:**
1. **Image Upload**: Images are uploaded through the prediction API
2. **Feature Extraction**: Comprehensive features are extracted from each image
3. **Database Storage**: Features and predictions are stored in PostgreSQL
4. **Drift Analysis**: Regular analysis compares current vs. reference data
5. **Report Generation**: HTML reports are generated with visualizations
6. **Dashboard Updates**: Real-time dashboard shows current metrics

**Core Modules:**

* **monitoring.core.monitor**: Main orchestrator class
* **monitoring.core.drift_detector**: Drift detection algorithms
* **monitoring.core.feature_extractor**: Image feature extraction
* **monitoring.api.endpoints**: REST API endpoints

Feature Extraction
-----------------

The system extracts 20+ features from brain tumor images:

**Basic Image Features:**
* Width, height, channels
* File size in bytes
* Image format and metadata

**Statistical Features:**
* Brightness (mean, std)
* Contrast (mean, std)
* Entropy (information content)
* Skewness and kurtosis
* Mean and standard deviation intensity

**Tumor-Specific Features:**
* Tumor detection confidence
* Number of tumors detected
* Tumor area ratios
* Largest tumor area
* Tumor density
* Tumor location (x, y coordinates)
* Tumor shape regularity

**Quality Metrics:**
* Noise levels
* Artifact detection
* Image sharpness
* Compression artifacts

Example feature extraction:

.. code-block:: python

   from monitoring.core.monitor import BrainTumorImageMonitor

   monitor = BrainTumorImageMonitor(database_url)
   features = monitor.extract_brain_tumor_features(image_array)

   print(f"Brightness mean: {features['brightness_mean']}")
   print(f"Tumor confidence: {features['tumor_detection_confidence']}")

Drift Detection
--------------

The system implements multiple drift detection strategies:

**Statistical Drift Detection:**
* Compares current data distributions against reference datasets
* Uses mean, standard deviation, and distribution shape analysis
* Customizable thresholds for different features
* Clean dataset splitting to avoid overlap

**Drift Scoring:**
* Combines mean and standard deviation differences
* Normalizes by reference standard deviation
* Provides interpretable drift scores
* Configurable significance thresholds

**Reference Data Management:**
* Uses oldest 50 records as reference dataset
* Current data uses newest 50 records
* Ensures no temporal overlap
* Automatic reference data updates

Example drift analysis:

.. code-block:: python

   # Analyze drift for last 7 days
   analysis = monitor.analyze_feature_drift(days=7)

   for feature, data in analysis.items():
       if data['significant_drift']:
           print(f"Drift detected in {feature}: {data['drift_score']:.2f}")

Reporting System
---------------

The system generates comprehensive HTML reports using Evidently AI:

**Report Types:**
* **Drift Reports**: Feature distribution comparisons
* **Data Quality Reports**: Missing values, outliers, completeness
* **Performance Reports**: Model accuracy and confidence trends
* **Summary Reports**: Executive summaries for stakeholders

**Report Features:**
* Interactive visualizations
* Statistical summaries
* Drift score explanations
* Export capabilities
* Automated scheduling

**Report Generation:**

.. code-block:: python

   # Generate drift report
   report_path = monitor.generate_brain_tumor_drift_report(days=7)
   print(f"Report saved to: {report_path}")

   # Serve report via API
   # GET /monitoring/report/{report_name}

Dashboard
---------

The monitoring dashboard provides real-time insights:

**Key Metrics:**
* Total predictions today
* Average confidence scores
* Most common prediction classes
* Drift detection status
* System health indicators

**Real-time Updates:**
* WebSocket connections for live updates
* Automatic refresh every 30 seconds
* Configurable update intervals
* Historical trend visualization

**Alert System:**
* Configurable drift thresholds
* Email notifications
* Slack/Teams integration
* Escalation procedures

Configuration
------------

**Environment Variables:**

.. code-block:: bash

   # Database connection
   DATABASE_URL=postgresql://user:password@host:5432/database

   # Drift detection settings
   DRIFT_THRESHOLD=1.0
   REFERENCE_DAYS=30
   CURRENT_DAYS=7

   # Feature extraction
   IMAGE_MAX_SIZE=10485760  # 10MB
   FEATURE_EXTRACTION_TIMEOUT=30

   # Reporting
   REPORTS_DIR=reports/monitoring
   REPORT_RETENTION_DAYS=30

**Drift Detection Configuration:**

.. code-block:: python

   # Customize drift detection
   monitor = BrainTumorImageMonitor(
       database_url=database_url,
       drift_threshold=0.8,  # More sensitive
       reference_days=60,    # More reference data
       current_days=14       # Longer current period
   )

**Feature Selection:**

.. code-block:: python

   # Focus on specific features
   key_features = [
       "brightness_mean",
       "contrast_mean",
       "entropy",
       "tumor_detection_confidence"
   ]

   # Custom drift analysis
   analysis = monitor.analyze_feature_drift(
       days=7,
       features=key_features
   )

Performance Monitoring
---------------------

**System Metrics:**
* API response times
* Database query performance
* Memory usage
* CPU utilization
* Disk I/O

**Application Metrics:**
* Prediction throughput
* Feature extraction time
* Drift analysis duration
* Report generation time
* Error rates

**Monitoring Tools:**
* Built-in logging
* Prometheus metrics
* Grafana dashboards
* Health checks

Integration
----------

**ML Pipeline Integration:**

.. code-block:: python

   # In your prediction pipeline
   from monitoring.core.monitor import BrainTumorImageMonitor

   monitor = BrainTumorImageMonitor(database_url)

   # Log prediction for monitoring
   monitor.log_prediction(image, prediction_result)

**API Integration:**

.. code-block:: python

   import requests

   # Get dashboard data
   response = requests.get("http://localhost:8000/monitoring/dashboard")
   dashboard_data = response.json()

   # Generate drift report
   response = requests.get("http://localhost:8000/monitoring/drift-report?days=7")
   report_info = response.json()

**WebSocket Integration:**

.. code-block:: javascript

   const ws = new WebSocket('ws://localhost:8000/ws');

   ws.onmessage = function(event) {
     const data = JSON.parse(event.data);

     if (data.type === 'drift_alert') {
       console.log('Drift detected:', data.feature);
     }
   };

Troubleshooting
--------------

**Common Issues:**

**No Drift Detection:**
* Check if sufficient data exists
* Verify reference/current data split
* Review drift threshold settings
* Check feature extraction

**High Memory Usage:**
* Reduce batch sizes
* Optimize database queries
* Implement data retention policies
* Monitor memory leaks

**Slow Report Generation:**
* Increase timeout settings
* Optimize Evidently configuration
* Use background processing
* Implement caching

**Database Connection Issues:**
* Verify connection string
* Check database permissions
* Monitor connection pool
* Review query performance

**Getting Help:**
* Check logs: `tail -f logs/monitoring.log`
* Review configuration
* Test with sample data
* Contact support team

Best Practices
-------------

**Data Management:**
* Regular backup of monitoring data
* Implement data retention policies
* Monitor database size
* Optimize query performance

**Drift Detection:**
* Start with conservative thresholds
* Monitor drift patterns over time
* Adjust thresholds based on domain knowledge
* Document drift events and responses

**Reporting:**
* Schedule regular report generation
* Archive old reports
* Share reports with stakeholders
* Track report usage and feedback

**Performance:**
* Monitor system resources
* Optimize feature extraction
* Use background processing for heavy tasks
* Implement caching where appropriate

**Security:**
* Secure database connections
* Implement access controls
* Monitor for suspicious activity
* Regular security updates

For detailed configuration options, see :doc:`configuration`.

For troubleshooting guides, see :doc:`troubleshooting`.

For API reference, see :doc:`../api/index`.
