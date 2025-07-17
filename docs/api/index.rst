API Reference
============

The Brain Tumor Monitoring System provides a comprehensive REST API for monitoring operations, prediction logging, and drift analysis.

.. toctree::
   :maxdepth: 2
   :caption: API Documentation:

   endpoints
   models
   authentication
   errors

Overview
--------

The API is built using FastAPI and provides the following main categories of endpoints:

* **Health & Status**: System health checks and status information
* **Prediction**: Image prediction and logging endpoints
* **Monitoring**: Dashboard data and drift analysis
* **Reports**: HTML report generation and serving
* **Patients**: Patient data management (if applicable)

Base URL
--------

* **Development**: `http://localhost:8000`
* **Production**: `https://your-domain.com`

Authentication
-------------

Currently, the API uses a simple authentication scheme. For production deployments, consider implementing:

* JWT tokens
* API keys
* OAuth 2.0
* Role-based access control

Content Types
------------

* **Request**: `application/json` for JSON data, `multipart/form-data` for file uploads
* **Response**: `application/json` for JSON responses, `text/html` for reports

Rate Limiting
-------------

* **Default**: 100 requests per minute per IP
* **Prediction endpoints**: 50 requests per minute
* **Report generation**: 10 requests per minute

Error Handling
-------------

The API uses standard HTTP status codes:

* **200**: Success
* **400**: Bad Request
* **401**: Unauthorized
* **404**: Not Found
* **422**: Validation Error
* **500**: Internal Server Error

Response Format
--------------

**Success Response:**

.. code-block:: json

   {
     "status": "success",
     "data": {...},
     "message": "Operation completed successfully"
   }

**Error Response:**

.. code-block:: json

   {
     "status": "error",
     "error": "Error description",
     "details": {...}
   }

Quick Start
-----------

**1. Health Check**

.. code-block:: bash

   curl http://localhost:8000/health

**2. Get Dashboard Data**

.. code-block:: bash

   curl http://localhost:8000/monitoring/dashboard

**3. Generate Drift Report**

.. code-block:: bash

   curl "http://localhost:8000/monitoring/drift-report?days=7"

**4. Upload Image for Prediction**

.. code-block:: bash

   curl -X POST http://localhost:8000/predict \
     -F "file=@image.jpg"

Interactive Documentation
-----------------------

The API provides interactive documentation at:

* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:

* Explore all available endpoints
* Test API calls directly from the browser
* View request/response schemas
* Download OpenAPI specification

SDK Examples
------------

**Python Client Example:**

.. code-block:: python

   import requests

   # Health check
   response = requests.get("http://localhost:8000/health")
   print(response.json())

   # Upload image
   with open("image.jpg", "rb") as f:
       files = {"file": f}
       response = requests.post("http://localhost:8000/predict", files=files)
       print(response.json())

**JavaScript Client Example:**

.. code-block:: javascript

   // Health check
   fetch('http://localhost:8000/health')
     .then(response => response.json())
     .then(data => console.log(data));

   // Upload image
   const formData = new FormData();
   formData.append('file', fileInput.files[0]);

   fetch('http://localhost:8000/predict', {
     method: 'POST',
     body: formData
   })
   .then(response => response.json())
   .then(data => console.log(data));

**cURL Examples:**

.. code-block:: bash

   # Health check
   curl -X GET "http://localhost:8000/health"

   # Get monitoring dashboard
   curl -X GET "http://localhost:8000/monitoring/dashboard"

   # Generate drift report
   curl -X GET "http://localhost:8000/monitoring/drift-report?days=7"

   # Upload image for prediction
   curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg"

Testing
-------

**Unit Tests:**

.. code-block:: bash

   pytest tests/integrationtests/test_api_*.py

**Integration Tests:**

.. code-block:: bash

   pytest tests/integrationtests/ -v

**Load Testing:**

.. code-block:: bash

   # Install locust
   pip install locust

   # Run load test
   locust -f tests/performance_tests/locustfile.py

Performance
-----------

**Response Times:**
* Health check: < 50ms
* Dashboard data: < 200ms
* Drift analysis: < 2s
* Report generation: < 5s
* Image prediction: < 3s

**Throughput:**
* Concurrent requests: 100+
* Database connections: 20
* File upload size: 10MB max

Monitoring
----------

The API includes built-in monitoring:

* **Request logging**: All requests are logged with timing
* **Error tracking**: Detailed error logs with stack traces
* **Performance metrics**: Response times and throughput
* **Health checks**: Database connectivity and service status

For detailed endpoint documentation, see :doc:`endpoints`.

For data models and schemas, see :doc:`models`.

For authentication details, see :doc:`authentication`.

For error handling, see :doc:`errors`.
