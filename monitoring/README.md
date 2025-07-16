# Brain Tumor Monitoring System

A comprehensive monitoring and drift detection system for brain tumor image classification models.

## 🏗️ Architecture

```
monitoring/
├── core/                    # Core monitoring logic
│   ├── monitor.py          # Main orchestrator
│   ├── feature_extractor.py # Image feature extraction
│   └── drift_detector.py   # Drift detection algorithms
├── api/                    # REST API endpoints
│   ├── main.py            # FastAPI application
│   └── endpoints.py       # API routes
├── database/              # Database models and migrations
├── reports/               # Generated drift reports
├── tests/                 # Unit tests
└── requirements.txt       # Dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/monitoring"
```

### 3. Run the Service
```bash
uvicorn monitoring.api.main:app --host 0.0.0.0 --port 8000
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/monitoring/dashboard` | GET | Dashboard data |
| `/monitoring/drift-report` | GET | Generate drift report |
| `/monitoring/feature-analysis` | GET | Feature drift analysis |
| `/monitoring/data-quality` | GET | Data quality tests |

## 🔍 Features

### Image Feature Extraction
- **Basic Features**: Width, height, channels, file size
- **Statistical Features**: Brightness, contrast, entropy, skewness, kurtosis
- **Tumor-Specific Features**: Detection confidence, tumor area, location, shape

### Drift Detection
- **Clean Reference/Current Split**: No overlap between datasets
- **Statistical Analysis**: Mean, standard deviation comparisons
- **Drift Scoring**: Customizable thresholds
- **HTML Reports**: Evidently-generated visualizations

### Monitoring Dashboard
- **Real-time Metrics**: Predictions, confidence scores, class distributions
- **Drift Alerts**: Automatic detection of significant drift
- **Historical Tracking**: Trend analysis over time

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t brain-tumor-monitoring .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  brain-tumor-monitoring
```

## 🧪 Testing

### Run Tests
```bash
pytest monitoring/tests/
```

### Test Coverage
```bash
pytest --cov=monitoring monitoring/tests/
```

## 📈 Cloud Deployment

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitoring-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: monitoring
  template:
    metadata:
      labels:
        app: monitoring
    spec:
      containers:
      - name: monitoring
        image: brain-tumor-monitoring:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

### AWS Lambda
```python
import json
from monitoring.core.monitor import BrainTumorImageMonitor

def lambda_handler(event, context):
    monitor = BrainTumorImageMonitor(os.environ['DATABASE_URL'])
    analysis = monitor.analyze_feature_drift()
    return {
        'statusCode': 200,
        'body': json.dumps(analysis)
    }
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `DRIFT_THRESHOLD`: Drift detection sensitivity (default: 1.0)
- `REPORTS_DIR`: Directory for HTML reports (default: reports/monitoring)

### Database Schema
```sql
CREATE TABLE predictions_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    prediction_confidence FLOAT,
    prediction_class VARCHAR(50),
    num_detections INTEGER,
    model_version VARCHAR(50),
    processing_time_ms INTEGER,
    image_width FLOAT,
    image_height FLOAT,
    image_channels FLOAT,
    image_size_bytes FLOAT,
    brightness_mean FLOAT,
    brightness_std FLOAT,
    contrast_mean FLOAT,
    contrast_std FLOAT,
    entropy FLOAT,
    skewness FLOAT,
    kurtosis FLOAT,
    mean_intensity FLOAT,
    std_intensity FLOAT,
    tumor_area_ratio FLOAT,
    tumor_detection_confidence FLOAT,
    num_tumors_detected FLOAT,
    largest_tumor_area FLOAT,
    tumor_density FLOAT,
    tumor_location_x FLOAT,
    tumor_location_y FLOAT,
    tumor_shape_regularity FLOAT
);
```

## 📝 Usage Examples

### Feature Analysis
```python
from monitoring.core.monitor import BrainTumorImageMonitor

monitor = BrainTumorImageMonitor("postgresql://localhost/monitoring")
analysis = monitor.analyze_feature_drift(days=7)

for feature, data in analysis.items():
    if data['significant_drift']:
        print(f"Drift detected in {feature}: {data['drift_score']:.2f}")
```

### Drift Report Generation
```python
report_path = monitor.generate_brain_tumor_drift_report(days=7)
print(f"Report generated: {report_path}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
