API Endpoints
=============

This document provides detailed information about all available API endpoints in the Brain Tumor Monitoring System.

Health & Status Endpoints
------------------------

Health Check
^^^^^^^^^^^

**Endpoint:** `GET /health`

**Description:** Check the health status of the API and its dependencies.

**Response:**

.. code-block:: json

   {
     "status": "ok",
     "message": "Backend is running",
     "timestamp": "2025-01-13T20:00:00Z",
     "version": "1.0.0"
   }

**Status Codes:**

* `200`: Service is healthy
* `503`: Service is unhealthy

**Example:**

.. code-block:: bash

   curl http://localhost:8000/health

Root Endpoint
^^^^^^^^^^^^^

**Endpoint:** `GET /`

**Description:** Get basic information about the API and available endpoints.

**Response:**


.. code-block:: json

   {
     "message": "Brain Tumor Monitoring System API",
     "version": "1.0.0",
     "endpoints": {
       "health": "/health",
       "predict": "/predict",
       "monitoring": "/monitoring/*",
       "patients": "/patients/*"
     }
   }

Prediction Endpoints
-------------------

Image Prediction
^^^^^^^^^^^^^^^

**Endpoint:** `POST /predict`

**Description:** Upload an image and get brain tumor prediction results.

**Request:**

* **Content-Type:** `multipart/form-data`
* **Body:** Form data with `file` field containing image

**Parameters:**

* `file` (required): Image file (JPG, PNG, BMP supported)
* `max_size`: 10MB

**Response:**

.. code-block:: json

   {
     "status": "success",
     "prediction": {
       "class": "malignant",
       "confidence": 0.85,
       "num_detections": 2,
       "processing_time_ms": 1200
     },
     "image_features": {
       "brightness_mean": 125.5,
       "contrast_mean": 45.2,
       "entropy": 7.8
     }
   }

**Status Codes:**

* `200`: Prediction successful
* `400`: Invalid file or format
* `413`: File too large
* `500`: Prediction failed

**Example:**

.. code-block:: bash

   curl -X POST http://localhost:8000/predict \
     -F "file=@brain_scan.jpg"

Monitoring Endpoints
-------------------

Dashboard Data
^^^^^^^^^^^^^

**Endpoint:** `GET /monitoring/dashboard`

**Description:** Get real-time monitoring dashboard data.

**Response:**

.. code-block:: json

   {
     "total_predictions_today": 150,
     "average_confidence": 0.82,
     "most_common_class": "benign",
     "avg_tumor_confidence": 0.75,
     "malignant_count": 45,
     "benign_count": 85,
     "normal_count": 20,
     "last_drift_check": "2025-01-13T20:00:00Z",
     "alerts": []
   }

**Status Codes:**

* `200`: Dashboard data retrieved
* `500`: Error retrieving data

**Example:**

.. code-block:: bash

   curl http://localhost:8000/monitoring/dashboard

Drift Report Generation
^^^^^^^^^^^^^^^^^^^^^^

**Endpoint:** `GET /monitoring/drift-report`

**Description:** Generate HTML drift report for specified time period.

**Query Parameters:**

* `days` (optional): Number of days to analyze (default: 7)

**Response:**

.. code-block:: json

   {
     "message": "Brain tumor drift report generated successfully",
     "report_path": "reports/monitoring/brain_tumor_drift_report_20250113_200000.html",
     "days_analyzed": 7,
     "drift_summary": {
       "total_features": 20,
       "drifted_features_count": 3,
       "drift_percentage": 15.0
     }
   }

**Status Codes:**

* `200`: Report generated successfully
* `400`: Insufficient data for analysis
* `500`: Error generating report

**Example:**

.. code-block:: bash

   curl "http://localhost:8000/monitoring/drift-report?days=14"

Feature Analysis
^^^^^^^^^^^^^^^

**Endpoint:** `GET /monitoring/feature-analysis`

**Description:** Get detailed feature drift analysis.

**Query Parameters:**

* `days` (optional): Number of days to analyze (default: 7)

**Response:**

.. code-block:: json

   {
     "brightness_mean": {
       "reference_mean": 125.5,
       "reference_std": 15.2,
       "current_mean": 135.8,
       "current_std": 18.1,
       "mean_difference": 10.3,
       "std_difference": 2.9,
       "drift_score": 1.2,
       "significant_drift": true
     },
     "contrast_mean": {
       "reference_mean": 45.2,
       "reference_std": 8.5,
       "current_mean": 42.1,
       "current_std": 7.8,
       "mean_difference": 3.1,
       "std_difference": 0.7,
       "drift_score": 0.4,
       "significant_drift": false
     }
   }

**Status Codes:**

* `200`: Analysis completed
* `400`: Insufficient data
* `500`: Analysis error

**Example:**

.. code-block:: bash

   curl "http://localhost:8000/monitoring/feature-analysis?days=7"

Data Quality Tests
^^^^^^^^^^^^^^^^^

**Endpoint:** `GET /monitoring/data-quality`

**Description:** Run data quality tests and return results.

**Response:**

.. code-block:: json

   {
     "data_quality": true,
     "missing_values_test": true,
     "outliers_test": true,
     "timestamp": "2025-01-13T20:00:00Z",
     "details": {
       "missing_values_percentage": 0.1,
       "outlier_percentage": 2.5,
       "data_completeness": 99.9
     }
   }

**Status Codes:**

* `200`: Tests completed
* `500`: Test error

**Example:**

.. code-block:: bash

   curl http://localhost:8000/monitoring/data-quality

Report Serving
^^^^^^^^^^^^^

**Endpoint:** `GET /monitoring/report/{report_name}`

**Description:** Serve generated HTML reports.

**Path Parameters:**

* `report_name`: Name of the report file

**Response:**

* **Content-Type:** `text/html`
* **Body:** HTML report content

**Status Codes:**

* `200`: Report served
* `404`: Report not found

**Example:**

.. code-block:: bash

   curl http://localhost:8000/monitoring/report/brain_tumor_drift_report_20250113_200000.html

Patient Management Endpoints
---------------------------

Get All Patients
^^^^^^^^^^^^^^^

**Endpoint:** `GET /patients`

**Description:** Get list of all patients.

**Response:**

.. code-block:: json

   {
     "patients": [
       {
         "id": 1,
         "name": "John Doe",
         "age": 45,
         "diagnosis_date": "2025-01-10",
         "last_scan_date": "2025-01-13"
       }
     ],
     "total_count": 1
   }

**Status Codes:**

* `200`: Patients retrieved
* `500`: Database error

**Example:**

.. code-block:: bash

   curl http://localhost:8000/patients

Get Patient by ID
^^^^^^^^^^^^^^^^

**Endpoint:** `GET /patients/{id}`

**Description:** Get specific patient information.

**Path Parameters:**

* `id`: Patient ID

**Response:**

.. code-block:: json

   {
     "id": 1,
     "name": "John Doe",
     "age": 45,
     "diagnosis_date": "2025-01-10",
     "last_scan_date": "2025-01-13",
     "scans": [
       {
         "id": 1,
         "date": "2025-01-13",
         "prediction": "benign",
         "confidence": 0.85
       }
     ]
   }

**Status Codes:**

* `200`: Patient found
* `404`: Patient not found
* `500`: Database error

**Example:**

.. code-block:: bash

   curl http://localhost:8000/patients/1

Error Handling
-------------

All endpoints follow consistent error handling patterns:

**Validation Errors (422):**

.. code-block:: json

   {
     "detail": "Invalid request data",
     "errors": [
       {
         "loc": ["body", "file"],
         "msg": "field required",
         "type": "value_error.missing"
       }
     ]
   }

**Not Found Errors (404):**

.. code-block:: json

   {
     "detail": "Resource not found"
   }

**Internal Server Errors (500):**

.. code-block:: json

   {
     "detail": "Internal server error"
   }

Rate Limiting
-------------

The API implements rate limiting to prevent abuse:

* **Default limit**: 100 requests per minute per IP

* **Prediction endpoints**: 50 requests per minute
* **Report generation**: 10 requests per minute

When rate limit is exceeded:

.. code-block:: json

   {
     "detail": "Rate limit exceeded",
     "retry_after": 60
   }

Response Headers
---------------

All responses include standard headers:

* `Content-Type`: Response content type
* `X-Request-ID`: Unique request identifier
* `X-Response-Time`: Response time in milliseconds
* `X-Rate-Limit-Remaining`: Remaining requests in current window

CORS Support
-----------

The API supports Cross-Origin Resource Sharing (CORS):

* **Allowed Origins**: Configurable (default: all origins)
* **Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
* **Allowed Headers**: Content-Type, Authorization
* **Credentials**: Supported

WebSocket Support
----------------

For real-time updates, the API supports WebSocket connections:

* **Endpoint**: `ws://localhost:8000/ws`
* **Events**: drift_alerts, prediction_updates, system_status
* **Authentication**: Same as REST API

Example WebSocket usage:
 javascript

   const ws = new WebSocket('ws://localhost:8000/ws');

   ws.onmessage = function(event) {
     const data = JSON.parse(event.data);
     console.log('Received:', data);
   };
