# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/d5f1784b-ec90-493d-973d-0dbcd80182bd

## Project Structure

This project is organized into distinct directories to support a full-stack application with an MLOps pipeline. Below is an overview of the key directories and their purposes:

```
smart-health-predictor/
├── .github/                  # GitHub Actions and Dependabot configurations
│   ├── dependabot.yaml
│   └── workflows/
│       └── tests.yaml        # CI/CD workflows for testing
├── configs/                  # Configuration files
│   ├── data/                 # Data-related configurations
│   └── model/                # Model-related configurations
├── data/                     # Data directory
│   ├── processed/            # Processed and cleaned data
│   └── raw/                  # Raw, uncleaned data
├── dockerfiles/              # Dockerfiles for containerizing services
│   ├── api.Dockerfile        # Dockerfile for the prediction API
│   └── train.Dockerfile      # Dockerfile for model training
├── docs/                     # Project documentation
│   ├── mkdocs.yml            # MkDocs configuration
│   └── source/               # Documentation source files
│       └── index.md
├── models/                   # Directory for trained model artifacts
├── notebooks/                # Jupyter notebooks for experimentation and analysis
├── reports/                  # Generated reports and figures
│   └── figures/
├── src/                      # Source code
│   ├── frontend/             # Frontend React application code
│   │   ├── components/       # Reusable UI components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── lib/              # Utility functions and shared configurations
│   │   ├── pages/            # Top-level page components (e.g., Index.tsx)
│   │   ├── types/            # TypeScript type definitions
│   │   ├── App.css           # Main application CSS
│   │   ├── App.tsx           # Main application component
│   │   ├── index.css         # Global styles
│   │   ├── main.tsx          # Application entry point
│   │   └── vite-env.d.ts     # Vite environment type definitions
│   └── ml_backend/           # Machine Learning Backend (Python)
│       ├── __init__.py       # Makes ml_backend a Python package
│       ├── api.py            # FastAPI application for model serving
│       ├── data.py           # Data loading and initial processing scripts
│       ├── evaluate.py       # Model evaluation scripts
│       ├── features.py       # Feature engineering scripts
│       ├── models.py         # Model definition, training, and prediction logic
│       ├── train.py          # Main script for orchestrating model training
│       └── visualize.py      # Data and model visualization scripts
├── tests/                    # Unit and integration tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_data.py
│   └── test_model.py
├── .env                      # Environment variables (ignored by Git)
├── .gitignore                # Specifies intentionally untracked files to ignore
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
├── LICENSE                   # Project licensing information
├── pyproject.toml            # Python project metadata and build system
├── README.md                 # Project overview and instructions
├── requirements.txt          # Python dependencies for the project
├── requirements_dev.txt      # Development Python dependencies
├── tasks.py                  # Automation scripts (e.g., using Invoke)
└── vite.config.ts            # Vite configuration for the frontend
```

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/d5f1784b-ec90-493d-973d-0dbcd80182bd) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/d5f1784b-ec90-493d-973d-0dbcd80182bd) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/tips-tricks/custom-domain#step-by-step-guide)
