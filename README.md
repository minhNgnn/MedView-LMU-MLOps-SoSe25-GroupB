This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS
- FastAPI (Python backend)
- Ultralytics YOLO (ML)

## Codebase Structure

```
.github/                  # GitHub Actions and Dependabot configurations
│   ├── dependabot.yaml
│   └── workflows/
│       └── tests.yaml        # CI/CD workflows for testing
backend/                  # Backend API (FastAPI)
│   ├── src/
│   │   └── api.py         # FastAPI application for model serving
│   └── requirements.txt   # Backend dependencies
frontend/                 # Frontend React application
│   ├── src/               # React source code
│   ├── package.json       # Frontend dependencies
│   └── ...
ml/                      # Machine Learning logic (Python)
│   ├── data.py           # Data loading and initial processing scripts
│   ├── evaluate.py       # Model evaluation scripts
│   ├── features.py       # Feature engineering scripts
│   ├── models.py         # Model definition, training, and prediction logic
│   ├── train.py          # Main script for orchestrating model training
│   ├── visualize.py      # Data and model visualization scripts
│   ├── requirements.txt  # ML dependencies
│   └── configs/          # ML configs (e.g., sweep.yaml, model configs)
│   └── models/           # Saved model weights/artifacts
│   └── notebooks/        # Jupyter notebooks for experimentation and analysis
reports/                  # Generated reports and figures for the whole project
│   └── figures/
docker/                   # Dockerfiles, docker-compose setups
│   └── ...
tests/                    # Unit and integration tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_data.py
│   └── test_model.py
.gitignore                # Specifies intentionally untracked files to ignore
.pre-commit-config.yaml   # Pre-commit hooks configuration
LICENSE                   # Project licensing information
pyproject.toml            # Python project metadata and build system
README.md                 # Project overview and instructions
requirements_dev.txt      # Development Python dependencies (root)
tasks.py                  # Automation scripts (e.g., using Invoke)
```

## How to run the web frontend locally

1. **Install dependencies**
   ```sh
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```sh
   npm run dev
   ```

3. **Open your browser** and go to the URL shown in the terminal (usually http://localhost:8080).

The frontend code is located in `frontend/src/`. The entry point is `frontend/src/main.tsx` and the main HTML file is `frontend/src/index.html`.

## How to run the backend API locally

1. **Install dependencies**
   ```sh
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server**
   ```sh
   uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
   ```

The backend entry point is `backend/src/api.py`.

## How to run ML scripts

1. **Install ML dependencies**
   ```sh
   cd ml
   pip install -r requirements.txt
   ```

2. **Run training, evaluation, or other scripts as needed**
   ```sh
   python train.py
   python evaluate.py
   # etc.
   ```
