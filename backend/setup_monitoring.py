#!/usr/bin/env python3
"""
Setup script for the data drift monitoring system.
This script initializes the database tables and sets up the monitoring infrastructure.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Add the backend directory to the Python path
sys.path.append(str(Path(__file__).parent))

load_dotenv()

def setup_database():
    """Set up the database tables for monitoring."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ DATABASE_URL environment variable is not set")
        return False
    
    try:
        engine = create_engine(database_url)
        
        # Read the migration SQL file
        migration_file = Path(__file__).parent / "migrations" / "create_monitoring_tables.sql"
        
        if not migration_file.exists():
            print(f"❌ Migration file not found: {migration_file}")
            return False
        
        with open(migration_file, 'r') as f:
            sql_script = f.read()
        
        # Execute the migration
        with engine.connect() as conn:
            # Split the script into individual statements
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement:
                    try:
                        conn.execute(text(statement))
                        print(f"✅ Executed: {statement[:50]}...")
                    except SQLAlchemyError as e:
                        # Ignore errors for existing tables/indexes
                        if "already exists" in str(e).lower():
                            print(f"⚠️  Skipped (already exists): {statement[:50]}...")
                        else:
                            print(f"❌ Error executing: {statement[:50]}...")
                            print(f"   Error: {e}")
        
        conn.commit()
        print("✅ Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_reports_directory():
    """Create the reports directory structure."""
    try:
        reports_dir = Path("reports/monitoring")
        reports_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created reports directory: {reports_dir}")
        return True
    except Exception as e:
        print(f"❌ Failed to create reports directory: {e}")
        return False

def install_dependencies():
    """Install required Python dependencies."""
    try:
        import evidently
        import pandas
        import nltk
        print("✅ All monitoring dependencies are already installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install the required dependencies:")
        print("pip install evidently pandas nltk")
        return False

def download_nltk_data():
    """Download required NLTK data."""
    try:
        import nltk
        nltk.download("words", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download("omw-1.4", quiet=True)
        print("✅ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to download NLTK data: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Data Drift Monitoring System...")
    print("=" * 50)
    
    # Check dependencies
    if not install_dependencies():
        return False
    
    # Download NLTK data
    if not download_nltk_data():
        return False
    
    # Create reports directory
    if not create_reports_directory():
        return False
    
    # Setup database
    if not setup_database():
        return False
    
    print("=" * 50)
    print("✅ Data Drift Monitoring System setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start your FastAPI server: uvicorn backend.src.api:app --reload")
    print("2. Access monitoring endpoints:")
    print("   - Dashboard: GET /monitoring/dashboard")
    print("   - Data Quality: GET /monitoring/data-quality")
    print("   - Drift Report: GET /monitoring/drift-report")
    print("3. Add the MonitoringDashboard component to your frontend")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 