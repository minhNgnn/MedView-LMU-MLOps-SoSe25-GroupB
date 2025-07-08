This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## Codebase Structure

```
.github/                  # GitHub Actions and Dependabot configurations
│   ├── dependabot.yaml
│   └── workflows/
│       └── tests.yaml        # CI/CD workflows for testing
configs/                  # Configuration files
│   ├── data/             # Data-related configurations
│   └── model/            # Model-related configurations
data/                     # Data directory
│   ├── processed/        # Processed and cleaned data
│   └── raw/              # Raw, uncleaned data
dockerfiles/              # Dockerfiles for containerizing services
│   ├── api.Dockerfile    # Dockerfile for the prediction API
│   └── train.Dockerfile  # Dockerfile for model training
docs/                     # Project documentation
│   ├── mkdocs.yml        # MkDocs configuration
│   └── source/           # Documentation source files
│       └── index.md
models/                   # Directory for trained model artifacts
notebooks/                # Jupyter notebooks for experimentation and analysis
reports/                  # Generated reports and figures
│   └── figures/
src/
│   ├── frontend/         # Frontend React application code
│   │   ├── components/   # Reusable UI components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── lib/          # Utility functions and shared configurations
│   │   ├── pages/        # Top-level page components (e.g., Index.tsx)
│   │   ├── types/        # TypeScript type definitions
│   │   ├── App.css       # Main application CSS
│   │   ├── App.tsx       # Main application component
│   │   ├── index.css     # Global styles
│   │   ├── main.tsx      # Application entry point
│   │   └── vite-env.d.ts # Vite environment type definitions
│   └── ml_backend/       # Machine Learning Backend (Python)
│       ├── __init__.py   # Makes ml_backend a Python package
│       ├── api.py        # FastAPI application for model serving
│       ├── data.py       # Data loading and initial processing scripts
│       ├── evaluate.py   # Model evaluation scripts
│       ├── features.py   # Feature engineering scripts
│       ├── models.py     # Model definition, training, and prediction logic
│       ├── train.py      # Main script for orchestrating model training
│       └── visualize.py  # Data and model visualization scripts
tests/                    # Unit and integration tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_data.py
│   └── test_model.py
.env                      # Environment variables (ignored by Git)
.gitignore                # Specifies intentionally untracked files to ignore
.pre-commit-config.yaml   # Pre-commit hooks configuration
LICENSE                   # Project licensing information
pyproject.toml            # Python project metadata and build system
README.md                 # Project overview and instructions
requirements.txt          # Python dependencies for the project
requirements_dev.txt      # Development Python dependencies
tasks.py                  # Automation scripts (e.g., using Invoke)
vite.config.ts            # Vite configuration for the frontend
```

## How to run the web frontend locally

1. **Install dependencies**
   ```sh
   npm install
   ```

2. **Start the development server**
   ```sh
   npm run dev
   ```

3. **Open your browser** and go to the URL shown in the terminal (usually http://localhost:8080 or http://localhost:8081).

The frontend code is located in `src/frontend/`. The entry point is `src/frontend/main.tsx` and the main HTML file is `src/frontend/index.html`.

## How to run the app with Docker

You can run the full stack application (frontend and backend) using Docker and Docker Compose. This will build and start both the FastAPI backend and the frontend (served with nginx) in separate containers.

### 1. Build and run with Docker Compose

From the project root, run:

```sh
docker-compose up --build
```

- This command will build the images for both the API and frontend using the Dockerfiles in `dockerfiles/api.Dockerfile` and `dockerfiles/frontend.Dockerfile`.
- It will start both services as defined in `docker-compose.yml`.

### 2. Access the app

- **Frontend:** [http://localhost:8080](http://localhost:8080)
- **API:** [http://localhost:8000](http://localhost:8000)

### 3. Stopping the app

To stop the containers, press `Ctrl+C` in the terminal where Docker Compose is running. To remove the containers, run:

```sh
docker-compose down
```

### 4. Notes
- Make sure Docker is installed and running on your system.
- You can modify the Dockerfiles in the `dockerfiles/` directory if you need to customize the build process for the API or frontend.
- The `docker-compose.yml` file orchestrates the services and handles port mapping.
